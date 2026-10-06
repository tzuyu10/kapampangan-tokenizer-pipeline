"""Read-only observers for the pinned Transformers 4.48.3 beam-search implementation.

Keep only small vector slices and candidate lists, never full vocabulary scores.
Use under the translation service's model lock. All hooks are removed on exit.
"""
import math
from contextlib import contextmanager

import torch
from transformers import LogitsProcessorList


def number(value):
    value = float(value)
    return round(value, 5) if math.isfinite(value) else None


class GenerationTrace:
    def __init__(self, target, vector_width=4):
        self.target = target
        self.vector_width = vector_width
        self.embedding = []
        self.encoder = []
        self.steps = []
        self.final_candidates = []
        self.length_penalty = None

    def token(self, identifier):
        return dict(id=int(identifier), token=self.target.convert_ids_to_tokens(int(identifier)))

    def vectors(self, tensor):
        return [[number(v) for v in row] for row in tensor[0, :, :self.vector_width].detach().cpu().tolist()]

    def observe_scores(self, input_ids, scores):
        values, identifiers = torch.topk(scores, min(4, scores.shape[-1]), dim=-1)
        beams = []
        for index, (prefix, ids, vals) in enumerate(zip(input_ids.tolist(), identifiers.tolist(), values.tolist())):
            candidates = [dict(self.token(i), score=number(v)) for i, v in zip(ids, vals) if math.isfinite(v)]
            beams.append(dict(beam=index, prefix_ids=prefix,
                              text=self.target.decode(prefix, skip_special_tokens=True), candidates=candidates))
        self.steps.append(dict(step=len(self.steps) + 1, beams=beams, retained=[], shortlist=[]))
        return scores

    @contextmanager
    def capture(self, model):
        encoder = model.get_encoder()
        handles = []
        own_search = model.__dict__.get('_beam_search')
        had_search = '_beam_search' in model.__dict__
        original_search = model._beam_search

        def embeddings_hook(module, args, output):
            self.embedding = self.vectors(output)

        def encoder_hook(module, args, output):
            self.encoder = self.vectors(output.last_hidden_state)

        def observed_search(input_ids, beam_scorer, logits_processor, *args, **kwargs):
            original_process = beam_scorer.process
            own_process = beam_scorer.__dict__.get('process')
            had_process = 'process' in beam_scorer.__dict__

            def observed_process(input_ids, next_scores, next_tokens, next_indices, **process_kwargs):
                result = original_process(input_ids, next_scores, next_tokens, next_indices, **process_kwargs)
                step = self.steps[-1]
                for parent, token, score in zip(next_indices[0].tolist(), next_tokens[0].tolist(), next_scores[0].tolist()):
                    step['shortlist'].append(dict(self.token(token), from_beam=parent, score=number(score)))
                for slot, (parent, token, score) in enumerate(zip(result['next_beam_indices'].tolist(),
                        result['next_beam_tokens'].tolist(), result['next_beam_scores'].tolist())):
                    prefix = step['beams'][parent]['prefix_ids'] + [token]
                    step['retained'].append(dict(self.token(token), beam=slot, from_beam=parent,
                        score=number(score), text=self.target.decode(prefix, skip_special_tokens=True)))
                step['search_done'] = bool(beam_scorer.is_done)
                return result

            beam_scorer.process = observed_process
            try:
                # The observer is last, so it sees forced-language/EOS constraints too.
                processors = LogitsProcessorList([*logits_processor, self.observe_scores])
                output = original_search(input_ids, beam_scorer, processors, *args, **kwargs)
                self.length_penalty = beam_scorer.length_penalty
                # finalize() sorts a copy of these hypotheses; their real scores remain available.
                ranked = reversed(sorted(beam_scorer._beam_hyps[0].beams, key=lambda item: item[0]))
                self.final_candidates = [dict(ids=ids.tolist(), score=number(score), chosen=rank == 0,
                    text=self.target.decode(ids.tolist(), skip_special_tokens=True))
                    for rank, (score, ids, _) in enumerate(ranked)]
                return output
            finally:
                if had_process:
                    beam_scorer.process = own_process
                else:
                    del beam_scorer.process

        try:
            handles.append(encoder.embed_tokens.register_forward_hook(embeddings_hook))
            handles.append(encoder.register_forward_hook(encoder_hook))
            model._beam_search = observed_search
            yield self
        finally:
            for handle in handles:
                handle.remove()
            if had_search:
                model._beam_search = own_search
            else:
                del model._beam_search

    def finish(self, output_ids):
        """Mark the returned sequence retrospectively, not as greedy per-step choices."""
        for step in self.steps:
            step['final_choice'] = None
            for beam in step['beams']:
                prefix = beam['prefix_ids']
                length = len(prefix)
                beam['on_final_path'] = length < len(output_ids) and prefix == output_ids[:length]
                if beam['on_final_path']:
                    chosen = output_ids[length]
                    if step['final_choice'] is None:
                        step['final_choice'] = dict(self.token(chosen), from_beam=beam['beam'],
                            text=self.target.decode(output_ids[:length + 1], skip_special_tokens=True))
                    for candidate in beam['candidates']:
                        candidate['chosen'] = candidate['id'] == chosen
            for item in step['retained']:
                sequence = step['beams'][item['from_beam']]['prefix_ids'] + [item['id']]
                item['on_final_path'] = sequence == output_ids[:len(sequence)]
        return dict(vector_preview_dimensions=self.vector_width, embedding_vectors=self.embedding,
                    encoder_vectors=self.encoder, decoder_steps=self.steps,
                    final_candidates=self.final_candidates, length_penalty=self.length_penalty)
