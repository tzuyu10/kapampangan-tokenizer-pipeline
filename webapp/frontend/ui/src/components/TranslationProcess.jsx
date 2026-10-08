import { useState } from "react";

const tokenText = token => /^\s+$/.test(token) ? "␠" : token;
const vectorText = vector => `[${vector.map(value => value == null ? "N/A" : value.toFixed(4)).join(", ")}, …]`;
const scoreText = score => score == null ? "Blocked" : score <= -1e8 ? "Inactive initial slot" : score.toFixed(4);

function VectorTable({ process, encoder = false }) {
  const [showAll, setShowAll] = useState(false);
  const vectors = encoder ? process.encoder_vectors : process.embedding_vectors;
  if (!vectors?.length) return <p>Restart the backend and translate again to capture actual vector values.</p>;
  const tokens = [{ token: "<s>", id: 2 }, ...process.source_tokens, { token: "</s>", id: 3 }];
  const visible = showAll ? tokens : tokens.slice(0, 8);
  return <>
    <p className="process-hint">First {process.vector_preview_dimensions} of {process.embedding_dimension.toLocaleString()} actual values per position, rounded to 4 decimals. {encoder ? "The encoder changes the vectors, not the token IDs. Token labels identify their original positions." : "These are the embedding lookup outputs, including the model's embedding scale, before positional information is added."}</p>
    <div className="table-scroll"><table className="process-data-table">
      <thead><tr><th>Source piece</th><th>{encoder ? "Embedding vector →" : "Source ID → Model ID"}</th><th>{encoder ? "Encoder context vector" : "Embedding vector"}</th></tr></thead>
      <tbody>{visible.map((token, index) => <tr key={index}>
        <td><code>{tokenText(token.token)}</code></td>
        <td><code>{encoder ? vectorText(process.embedding_vectors[index]) : `${token.id} → ${process.model_source_ids[index]}`}</code></td>
        <td><code>{vectorText(vectors[index])}</code></td>
      </tr>)}</tbody>
    </table></div>
    {tokens.length > 8 && <button className="example-chip" onClick={() => setShowAll(!showAll)}>{showAll ? "Show fewer positions" : `Show all ${tokens.length} positions`}</button>}
  </>;
}

function DecoderTrace({ process }) {
  const [index, setIndex] = useState(0);
  const [beamIndex, setBeamIndex] = useState(null);
  const steps = process.decoder_steps;
  if (!steps?.length) return <p>Restart the backend and translate again to capture the decoder's actual candidates.</p>;
  const step = steps[Math.min(index, steps.length - 1)];
  const beam = step.beams[beamIndex ?? step.final_choice?.from_beam ?? 0];
  function move(value) { setIndex(value); setBeamIndex(null); }
  return <div className="decoder-trace">
    <p>The decoder predicts new IDs in the target vocabulary using the encoded input and the text generated so far. It keeps {process.beams} candidate sequences. The top four next-token candidates shown below are a small view of its vocabulary scores.</p>
    <div className="decoder-controls">
      <button className="example-chip" disabled={index === 0} onClick={() => move(index - 1)}>Previous</button>
      <label>Decoder step <select value={index} onChange={event => move(Number(event.target.value))} aria-label="Decoder step">
        {steps.map((item, i) => <option value={i} key={i}>{i + 1} of {steps.length - 1}{i === 0 ? " (Filipino tag)" : ""}</option>)}
      </select></label>
      <button className="example-chip" disabled={index === steps.length - 2} onClick={() => move(index + 1)}>Next</button>
    </div>
    <label className="decoder-beam-picker">Inspect incoming beam <select value={beam.beam} onChange={event => setBeamIndex(Number(event.target.value))} aria-label="Incoming beam">
      {step.beams.map(item => <option key={item.beam} value={item.beam}>Beam {item.beam + 1}{item.on_final_path ? " (matches final prefix)" : ""}</option>)}
    </select></label>
    <details><summary>Prefix token IDs</summary><p className="process-id-list">{beam.prefix_ids.join(" → ")}</p></details>
    <div className="table-scroll"><table className="process-data-table">
      <thead><tr><th>Next piece</th><th>Target ID</th><th>Next-token score</th><th>Final sequence</th></tr></thead>
      <tbody>{beam.candidates.map(item => <tr key={item.id} className={item.chosen ? "trace-selected" : ""}>
        <td><code>{item.token}</code></td><td>{item.id}</td><td>{scoreText(item.score)}</td><td>{item.chosen ? "Chosen in final output" : "Alternative"}</td>
      </tr>)}</tbody>
    </table></div>
    <p className="process-hint">Scores are log scores after generation constraints, not translation-quality scores. Higher is better. Step 1 forces tgl_Latn; it is not a learned word prediction.</p>
    {step.final_choice ? <p className="trace-choice">Final output uses <code>{step.final_choice.token}</code> (ID {step.final_choice.id}) here → <strong>{step.final_choice.text || "(control token, no readable text)"}</strong></p>
      : <p className="trace-choice">The final output has already ended. This step checks other unfinished candidates.</p>}
    {step.final_choice && beam.on_final_path && !beam.candidates.some(item => item.id === step.final_choice.id) && <p>The final choice is outside this beam's four displayed candidates.</p>}
    <h4>Four beam slots after this step</h4>
    <div className="table-scroll"><table className="process-data-table">
      <thead><tr><th>Beam</th><th>Appended piece / ID</th><th>Candidate text</th><th>Total score</th></tr></thead>
      <tbody>{step.retained.map(item => <tr key={item.beam} className={item.on_final_path ? "trace-selected" : ""}>
        <td>{item.beam + 1}</td><td><code>{item.token}</code> / {item.id}</td><td>{item.text || "(control tokens only)"}{item.on_final_path && <small className="trace-match">Matches final prefix</small>}</td><td>{scoreText(item.score)}</td>
      </tr>)}</tbody>
    </table></div>
    <p className="process-hint">Finished candidates ending in &lt;/s&gt; are handled separately. Early slots can be inactive or share the same prefix. {index === steps.length - 1 ? "Generation stops here, so these slots are not expanded again." : "These slots continue to the next step."} Highlighting follows the returned output after search finishes, not a greedy choice at each step.</p>
    {process.final_candidates?.length > 0 && <>
      <h4>Final candidates and selected translation</h4>
      <div className="table-scroll"><table className="process-data-table"><thead><tr><th>Rank</th><th>Candidate text</th><th>Final sequence score</th><th>Decision</th></tr></thead>
        <tbody>{process.final_candidates.map((item, i) => <tr key={i} className={item.chosen ? "trace-selected" : ""}><td>{i + 1}</td><td>{item.text || "(no readable text)"}</td><td>{scoreText(item.score)}</td><td>{item.chosen ? "Selected output" : "Alternative"}</td></tr>)}</tbody>
      </table>
      </div>
    </>}
  </div>;
}

function TargetDecoding({ process }) {
  const rows = process.target_decode_steps;
  if (!rows) return <TokenChips tokens={process.target_tokens.filter(token => !token.special)} />;
  return <div className="table-scroll"><table className="process-data-table">
    <thead><tr><th>Generated ID →</th><th>Target piece →</th><th>Readable text so far</th></tr></thead>
    <tbody>{rows.map((item, index) => <tr key={index}><td>{item.id}</td><td><code>{item.token}</code>{item.special && <small className="trace-match">Special token removed</small>}</td><td>{item.text || "(no readable text yet)"}</td></tr>)}</tbody>
  </table></div>;
}

function TokenChips({ tokens, showIds = true }) {
  return <div className="process-tokens">
    {tokens.map((item, index) => <span className={`process-token ${item.special ? "special" : ""}`} key={index}>
      <code>{/^\s+$/.test(item.token) ? "␠" : item.token}</code>
      {showIds && <small>{item.id}</small>}
    </span>)}
  </div>;
}

export default function TranslationProcess({ result, label }) {
  const process = result?.process;
  const steps = [
    { title: "Prepare the input", description: "Trim surrounding whitespace and normalize the Kapampangan text to a consistent Unicode form.",
      detail: process && <p className="process-example">{process.normalized_text}</p> },
    { title: "Tokenize Kapampangan", description: `${label} splits the text into learned pieces and assigns each piece a vocabulary ID.`,
      detail: process && <><TokenChips tokens={process.source_tokens} />
        <details><summary>IDs sent to the model</summary><p className="process-id-list">{process.model_source_ids.join(" · ")}</p>
        </details></> },
    { title: "Look up source embeddings", description: "Each source ID selects a learned number vector that the model can use.",
      detail: process && <><p className="process-fact">{process.model_source_ids.length} input IDs → {process.model_source_ids.length} vectors of {process.embedding_dimension.toLocaleString()} values</p><VectorTable key={`${label}:${process.input_text}`} process={process} /></> },
    { title: "Encode the sentence", description: "The encoder combines each token with its position and surrounding context.",
      detail: process && <><p className="process-fact">{process.encoder_layers} NLLB encoder layers → contextual representations</p><VectorTable key={`${label}:${process.input_text}`} process={process} encoder /></> },
    { title: "Generate with the decoder", description: "Using the encoder context and tokens generated so far, the decoder predicts the next target token repeatedly.",
      detail: process && <><p className="process-fact">Filipino target: {process.target_language} · {process.beams} beams · up to {process.max_new_tokens} new tokens</p>
        <DecoderTrace key={`${label}:${process.input_text}`} process={process} /></> },
    { title: "Decode with the target tokenizer", description: "The native NLLB target tokenizer turns generated IDs into text pieces, joins them, and removes special tokens.",
      detail: process && <><TargetDecoding process={process} /><p className="process-hint">▁ marks a word boundary in the target pieces. This tokenizer formats the output; the model generates the translation.</p></> },
    { title: "Display the Filipino output", description: "Show the decoded translation without manual post-editing.",
      detail: result && <p className="process-example process-final">{result.translation || "No visible text was generated."}</p> },
  ];

  return <section className="translation-process" aria-label={`${label} translation process`}>
    <h2 className="segmentation-heading">Translation Process <span className="process-condition">{label}</span></h2>
    <div className="segmentation-box">
      <div className="process-overview" aria-hidden="true">Input → Tokens → Embeddings → Encoder → Decoder → Target tokenizer → Filipino</div>
      <p className="process-intro">{process ? "Follow this input through real token IDs, small slices of actual model vectors, decoder candidates, and readable Filipino text." : result ? "Restart the backend and translate again to include token and process data with this result." : "Translate a sentence to see its actual tokens, vectors, decoder choices, and output in these steps."}</p>
      <ol className="process-steps">{steps.map(step => <li key={step.title}>
        <h3>{step.title}</h3><p>{step.description}</p>{step.detail}
      </li>)}</ol>
      <p className="process-footnote">Only the source embedding table was trained for each condition. The pretrained NLLB encoder, decoder, and target vocabulary remain frozen.</p>
    </div>
  </section>;
}
