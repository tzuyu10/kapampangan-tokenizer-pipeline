import { useEffect, useState } from "react";
import { getInitialMetrics } from "../api.js";

const format = value => Number.isFinite(value) ? value.toFixed(3) : "—";
const colors = ["morph", "plain", "uni"];

function Score({ value, color }) {
  return <span className="initial-score"><span className="initial-score-track" aria-hidden="true">
    <span className={`metric-bar-fill ${color}`} style={{ width: `${Math.max(0, Math.min(1, value)) * 100}%` }} />
  </span><span>{format(value)}</span></span>;
}

export default function InitialMetrics({ level }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  async function load() {
    setError("");
    try { setData(await getInitialMetrics()); }
    catch { setError("Initial metrics are unavailable. Start or restart the backend, then retry."); }
  }
  useEffect(() => { let active = true;
    getInitialMetrics().then(value => { if (active) setData(value); })
      .catch(() => { if (active) setError("Initial metrics are unavailable. Start or restart the backend, then retry."); });
    return () => { active = false; };
  }, []);
  const metrics = data?.[level];
  return <section className="card initial-metrics" aria-label={`${level} initial performance metrics`}>
    <div className="initial-metrics-heading"><h2>Initial performance metrics</h2>
      <span className="initial-metrics-badge">{level === "tokenizer" ? "Example-set diagnostic" : "Training & test evaluation"}</span></div>
    {error ? <p role="status">{error} <button className="example-chip" onClick={load}>Retry</button></p> : !metrics ? <p role="status">Loading saved metrics…</p> : <>
      <p className="initial-metrics-note">{metrics.scope}</p>
      <div className="initial-table-scroll"><table className="initial-metrics-table">
        <caption className="initial-metrics-note">{level === "tokenizer" ? `${metrics.word_occurrences} word occurrences · ${metrics.unique_words} unique words · 6,080-token vocabularies` : "Losses at the epoch with the lowest saved validation loss"}</caption>
        <thead><tr><th>Condition</th>{level === "tokenizer" ? <><th>Fertility ↓</th><th>Boundary F1 ↑</th><th>Consistency F1 ↑</th></> : <><th>Completed epochs</th><th>Best epoch</th><th>Training loss ↓</th><th>Validation loss ↓</th><th>BLEU ↑</th><th>chrF++ ↑</th></>}</tr></thead>
        <tbody>{metrics.rows.map((row, index) => <tr key={row.condition}><th scope="row">{row.condition}</th>
          {level === "tokenizer" ? <><td>{format(row.fertility)}</td><td><Score value={row.boundary_f1} color={colors[index]} /></td><td><Score value={row.consistency_f1} color={colors[index]} /></td></> : row.available ? <><td>{row.completed_epochs}</td><td>{row.best_epoch}</td><td>{format(row.train_loss)}</td><td>{format(row.validation_loss)}</td><td className={Number.isFinite(row.bleu) ? undefined : "initial-pending"} title={row.quality_reason}>{Number.isFinite(row.bleu) ? format(row.bleu) : row.quality_status}</td><td className={Number.isFinite(row.chrf_plus_plus) ? undefined : "initial-pending"} title={row.quality_reason}>{Number.isFinite(row.chrf_plus_plus) ? format(row.chrf_plus_plus) : row.quality_status}</td></> : <td colSpan={6}>{row.reason}</td>}
        </tr>)}</tbody>
      </table></div>
      {level === "translation" && metrics.rows.map(row => row.quality_reason
        ? <p className="initial-metrics-note" key={row.condition}>{row.condition}: {row.quality_reason}</p>
        : row.quality_status === "Evaluated" ? <p className="initial-metrics-note" key={row.condition}>{row.condition}: {row.evaluation_examples.toLocaleString()} test sentences, {row.evaluation_precision.toUpperCase()}, {row.evaluation_beams} beams, maximum {row.evaluation_max_new_tokens} new tokens.</p> : null)}
      <details className="initial-metrics-details"><summary>Metric Definition</summary>
        {level === "tokenizer" ? <><p>Fertility is subword pieces per word; lower means fewer pieces, not necessarily better morphology. F1 scores range from 0 to 1; higher means closer agreement with these reference boundaries and shared morphemes.</p><p>The MorphBPE row and the translation Morph-BPE bundle use the same weighted penalty-32 tokenizer. These tokenizer metrics describe segmentation; translation quality requires separate evaluation.</p><p>Source: <code>{metrics.source}</code></p>
          <details><summary>View diagnostic references</summary><p>{metrics.references.map((row, index) => <code key={index} className="initial-reference">{row.segmentation}</code>)}</p></details>
        </> : <><p>Training and validation loss measure target-token prediction error. They are not accuracy percentages and do not establish which model translates better.</p><p>{metrics.quality_note}</p></>}
      </details>
    </>}
  </section>;
}
