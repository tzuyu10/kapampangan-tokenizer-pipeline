import { useState } from "react";
import InitialMetrics from "../components/InitialMetrics.jsx";
import TranslationProcess from "../components/TranslationProcess.jsx";

const CONDITIONS = [{ key: "baseline", label: "Plain BPE" }, { key: "custom", label: "Morph-BPE" }];

export default function TranslationPerformancePage({ source, result, loading, error, onGoToTranslator }) {
  const [selected, setSelected] = useState("custom");
  const condition = CONDITIONS.find(item => item.key === selected);
  return <main className="page translation-performance-page">
    <h1 className="page-title">Translation Metrics & Process</h1>
    <p className="page-subtitle">Saved model diagnostics and the translation process for the input from Translator A/B.</p>
    <InitialMetrics level="translation" />
    <section className="card shared-translation-input">
      <div className="initial-metrics-heading"><h2>Shared Kapampangan input</h2><button className="example-chip" onClick={onGoToTranslator}>Open Translator A/B</button></div>
      <p className="process-example">{source.trim() || "Enter a sentence in Translator A/B to begin."}</p>
      <p className="initial-metrics-note">{loading ? "Translation is running. Results and process data will appear here when it finishes." : result ? "These observations come from the same translation run shown in Translator A/B." : "Run Compare translations in Translator A/B to populate the input metrics and process below."}</p>
    </section>
    {error && <div className="error-banner" role="alert">{error}</div>}
    <section className="card initial-metrics" aria-label="Shared input generation metrics">
      <h2>Current input metrics</h2>
      <div className="initial-table-scroll"><table className="initial-metrics-table"><thead><tr><th>Condition</th><th>Source tokens</th><th>Output tokens</th><th>Generation time</th></tr></thead>
        <tbody>{CONDITIONS.map(item => { const output = result?.[item.key]; return <tr key={item.key}><th scope="row">{item.label}</th><td>{output?.source_token_count ?? "Pending"}</td><td>{output?.output_token_count ?? "Pending"}</td><td>{output?.cache_hit ? "Cached" : output ? `${output.latency_ms} ms` : "Pending"}</td></tr>; })}</tbody>
      </table></div><p className="initial-metrics-note">Source counts include start/end tokens. Output counts exclude special tokens. Generation time is for each condition; cached output is not a new timing measurement. These statistics are not BLEU or chrF++.</p>
    </section>
    <div className="process-switch" role="group" aria-label="Translation process condition">
      <span>Explain the process for</span>{CONDITIONS.map(item => <button key={item.key} className={`example-chip ${selected === item.key ? "selected" : ""}`} aria-pressed={selected === item.key} onClick={() => setSelected(item.key)}>{item.label}</button>)}
    </div>
    {result && !result[selected] && <p className="translator-note">This condition did not return a result. Select the available condition or install both bundles.</p>}
    <TranslationProcess result={result?.[selected]} label={condition.label} />
  </main>;
}
