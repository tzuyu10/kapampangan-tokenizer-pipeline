import { useEffect, useState } from "react";
import { getInitialMetrics } from "../api.js";

const format = value => Number.isFinite(value) ? value.toFixed(3) : "Unavailable";
const colors = ["morph", "plain", "uni"];

function Score({ value, color }) {
  return <span className="initial-score"><span className="initial-score-track" aria-hidden="true">
    <span className={`metric-bar-fill ${color}`} style={{ width: `${Math.max(0, Math.min(1, value)) * 100}%` }} />
  </span><span>{format(value)}</span></span>;
}

export default function InitialMetrics({ level, tokenizerId = null }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [reload, setReload] = useState(0);
  const selectedTokenizer = level === "tokenizer" ? tokenizerId : null;
  useEffect(() => { let active = true;
    setData(null);
    setError("");
    getInitialMetrics(selectedTokenizer).then(value => { if (active) setData(value); })
      .catch(() => { if (active) setError("Initial metrics are unavailable. Start or restart the backend, then retry."); });
    return () => { active = false; };
  }, [selectedTokenizer, reload]);
  const metrics = data?.[level];
  const tokenizerComparison = data?.tokenizer_comparison || metrics?.tokenizer_comparison;
  const rowVocabularySizes = [...new Set((metrics?.rows || []).map(row => row.source_vocab_size).filter(Number.isFinite))];
  const vocabularySize = tokenizerComparison?.source_vocab_size
    ?? (rowVocabularySizes.length === 1 ? rowVocabularySizes[0] : null);
  const vocabularyCaption = Number.isFinite(vocabularySize) ? ` · ${vocabularySize.toLocaleString()}-token vocabularies` : "";
  return <section className="card initial-metrics" aria-label={`${level} initial performance metrics`}>
    <div className="initial-metrics-heading"><h2>Initial performance metrics</h2>
      <span className="initial-metrics-badge">{level === "tokenizer" ? "Example-set diagnostic" : "Training & saved evaluation"}</span></div>
    {error ? <p role="status">{error} <button className="example-chip" onClick={() => setReload(value => value + 1)}>Retry</button></p> : !metrics ? <p role="status">Loading saved metrics…</p> : <>
      <p className="initial-metrics-note">{level === "translation" ? "Saved training diagnostics for the active bundles. BLEU and chrF++ appear only when a verified evaluation matches the bundle. Loss is not translation accuracy." : metrics.scope}</p>
      {level === "tokenizer" && tokenizerComparison?.selected?.label && <p className="initial-metrics-note">Selected tokenizer: {tokenizerComparison.selected.label}. These diagnostic rows use the same matched artifacts as the live comparison.</p>}
      <div className="initial-table-scroll"><table className="initial-metrics-table">
        <caption className="initial-metrics-note">{level === "tokenizer" ? `${metrics.word_occurrences} word occurrences · ${metrics.unique_words} unique words${vocabularyCaption}` : "Losses at the epoch with the lowest saved validation loss"}</caption>
        <thead><tr><th>Condition</th>{level === "tokenizer" ? <><th>Fertility ↓</th><th>Boundary F1 ↑</th><th>Consistency F1 ↑</th></> : <><th>Completed epochs</th><th>Best epoch</th><th>Training loss ↓</th><th>Validation loss ↓</th><th>BLEU ↑</th><th>chrF++ ↑</th></>}</tr></thead>
        <tbody>{metrics.rows.map((row, index) => <tr key={row.condition}><th scope="row">{row.condition}
          {level === "tokenizer" && <div className="initial-metrics-note">
            {tokenizerComparison?.tokenizers?.[row.condition]?.label}
            {Number.isFinite(row.source_vocab_size) && <> · {row.source_vocab_size.toLocaleString()} tokens</>}
          </div>}
          {level === "translation" && <><div className="initial-metrics-note">{row.display_name || row.bundle?.display_name || "Active bundle"}</div>
            {(!Number.isFinite(row.bleu) || !Number.isFinite(row.chrf_plus_plus)) && <div className="initial-metrics-note">Evaluation {row.quality_status || "unavailable"}: {row.quality_reason || row.reason || "No verified evaluation matches this active bundle."}</div>}</>}
        </th>
          {level === "tokenizer" ? <><td>{format(row.fertility)}</td><td><Score value={row.boundary_f1} color={colors[index]} /></td><td><Score value={row.consistency_f1} color={colors[index]} /></td></> : row.available ? <><td>{row.completed_epochs}</td><td>{row.best_epoch}</td><td>{format(row.train_loss)}</td><td>{format(row.validation_loss)}</td></> : <td colSpan={4}>{row.reason}</td>}
          {level === "translation" && <><td>{format(row.bleu)}</td><td>{format(row.chrf_plus_plus)}</td></>}
        </tr>)}</tbody>
      </table></div>
      <details className="initial-metrics-details"><summary>Metric Definition</summary>
        {level === "tokenizer" ? <><p>Fertility is subword pieces per word; lower means fewer pieces, not necessarily better morphology. F1 scores range from 0 to 1; higher means closer agreement with these reference boundaries and shared morphemes.</p><p>The MorphBPE, Plain BPE and Unigram-LM rows use matched vocabulary sizes for the tokenizer last run on the Tokenization tab. These fixed demonstration references are rescored when that selection changes. Translation quality requires separate evaluation.</p><p>Source: <code>{metrics.source}</code></p>
          <details><summary>View diagnostic references</summary><p>{metrics.references.map((row, index) => <code key={index} className="initial-reference">{row.segmentation}</code>)}</p></details>
        </> : <><p>Training and validation loss measure target-token prediction error. They are not accuracy percentages and do not establish which model translates better.</p><p>BLEU and chrF++ are saved corpus scores on a 0 to 100 scale, comparing translations with Filipino references. The backend verifies that the evaluation belongs to the active bundle before displaying its scores. They do not score the current input or establish statistical significance. An unavailable score means that no matching verified evaluation is available.</p></>}
      </details>
    </>}
  </section>;
}
