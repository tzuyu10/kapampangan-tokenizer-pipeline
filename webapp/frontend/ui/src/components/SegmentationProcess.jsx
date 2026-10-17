// Renders the step-by-step merge trace for every word in the last tokenized
// input, in the same order the design mockup laid out for a single word:
// normalize -> word detection -> raw characters -> merge rules applied ->
// final token table. When the input had more than one word, each word gets
// its own card, stacked.

function rootAffixColoring(finalTokens) {
  if (finalTokens.length <= 1) {
    return finalTokens.map(() => "root");
  }
  let longestIdx = 0;
  finalTokens.forEach((t, i) => {
    if (t.token.length > finalTokens[longestIdx].token.length) longestIdx = i;
  });
  return finalTokens.map((_, i) => (i === longestIdx ? "root" : "affix"));
}

function WordTitle({ word }) {
  const roles = rootAffixColoring(word.final_tokens);
  return (
    <h3 className="word-card-title">
      {word.final_tokens.map((t, i) => (
        <span key={i} className={roles[i]}>
          {t.token}
        </span>
      ))}
    </h3>
  );
}

function MergeSteps({ steps }) {
  if (steps.length === 0) {
    return (
      <p className="merge-none">
        No merge rules were needed — this word was already a single learned vocabulary
        entry, or reduced to one unit before any rule applied.
      </p>
    );
  }
  return (
    <div className="merge-list">
      {steps.map((s) => (
        <div className="merge-line" key={s.step}>
          <span className="merge-badge">Merge #{s.step}</span>
          <span>
            <b>{s.chosen.left}</b> + <b>{s.chosen.right}</b> &rarr; <b>{s.chosen.result}</b>
          </span>
          <span className="merge-rank">(learned rule #{s.chosen.rank})</span>
        </div>
      ))}
    </div>
  );
}

function FinalTokenTable({ tokens }) {
  return (
    <table className="token-table">
      <thead>
        <tr>
          <th>Token</th>
          <th>Vocabulary ID</th>
          <th>Type</th>
        </tr>
      </thead>
      <tbody>
        {tokens.map((t, i) => (
          <tr key={i}>
            <td>{t.token}</td>
            <td>{t.id}</td>
            <td>{t.kind === "merge" ? "learned merge" : t.kind}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function UnigramWordCard({ word }) {
  const units = word.initial_units || word.characters || Array.from(word.surface);
  return (
    <div className="word-card">
      <div className="word-card-header">
        <h3 className="word-card-title">{word.surface}</h3>
      </div>
      <div className="step">
        <p className="step-label">1. Normalized word</p>
        <p className="step-value">{word.surface}</p>
      </div>
      <div className="step">
        <p className="step-label">2. Input characters</p>
        <div className="chars-row">{units.join(" | ")}</div>
      </div>
      <div className="step">
        <p className="step-label">3. Select learned pieces with Unigram-LM</p>
        <p className="step-value">
          Learned piece log-probabilities score possible segmentations. Viterbi decoding
          selects the highest-scoring path. The table shows the actual selected pieces.
        </p>
      </div>
      <div className="step" style={{ marginBottom: 0 }}>
        <p className="step-label">4. Final token output</p>
        <FinalTokenTable tokens={word.final_tokens} />
      </div>
    </div>
  );
}

function WordCard({ word, isFirst }) {
  return (
    <div className={`word-card ${isFirst ? "" : ""}`}>
      <div className="word-card-header">
        <div style={{ width: 70 }} />
        <WordTitle word={word} />
        <div className="legend">
          <span className="legend-item">
            <span className="legend-dot root" /> Root Word
          </span>
          <span className="legend-item">
            <span className="legend-dot affix" /> Affixes
          </span>
        </div>
      </div>

      <div className="step">
        <p className="step-label">1. Normalize</p>
        <p className="step-value">{word.surface}</p>
      </div>

      <div className="step">
        <p className="step-label">2. Word detection</p>
        <p className="step-value">
          {word.shortcut
            ? `Whole word "${word.surface}" already exists in the vocabulary — used directly, no merging needed.`
            : `Recognized as 1 word token: "${word.surface}"`}
        </p>
      </div>

      <div className="step">
        <p className="step-label">3. Start from raw characters</p>
        <div className="chars-row">
          {word.characters.map((c, i) => (
            <span key={i}>
              {c}
              {i < word.characters.length - 1 ? " | " : ""}
            </span>
          ))}
        </div>
      </div>

      <div className="step">
        <p className="step-label">4. Apply learned merge rules (lowest rank first)</p>
        <MergeSteps steps={word.steps} />
      </div>

      <div className="step" style={{ marginBottom: 0 }}>
        <p className="step-label">5. Final token output</p>
        <FinalTokenTable tokens={word.final_tokens} />
      </div>
    </div>
  );
}

function GoldSummary({ gold }) {
  if (!gold) return null;
  return (
    <div className="gold-summary">
      <p className="gold-summary-title">Gold morpheme check (from the | marks you entered)</p>
      <p style={{ margin: 0 }}>
        gold: {gold.gold_pieces.map((p) => p.join("-")).join("  ")}
      </p>
      <p className="process-hint">Boundary and consistency scores are shown in Tokenization Comparison &amp; Metrics.</p>
    </div>
  );
}

export default function SegmentationProcess({ result }) {
  if (!result || !result.words || result.words.length === 0) {
    return (
      <div className="segmentation-box">
        <p className="segmentation-empty">
          Type a Kapampangan word or sentence above and press Tokenize to see the step-by-step
          segmentation process here.
        </p>
      </div>
    );
  }

  return (
    <div className="segmentation-box">
      {result.words.map((word, i) => result.algorithm === "unigram_lm"
        ? <UnigramWordCard key={i} word={word} />
        : <WordCard key={i} word={word} isFirst={i === 0} />)}
      <GoldSummary gold={result.gold} />
    </div>
  );
}
