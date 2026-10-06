import { useEffect, useState } from "react";
import { CompareIcon, CopyIcon, TrashIcon } from "../components/icons.jsx";
import TranslationProcess from "../components/TranslationProcess.jsx";
import { compareTranslations, getTranslationStatus } from "../api.js";

const MAX_LEN = 500;
const CONDITIONS = [
  { key: "custom", label: "Morph-BPE + NLLB-200", short: "Morph-BPE", role: "Proposed system" },
  { key: "baseline", label: "Plain BPE + NLLB-200", short: "Plain BPE", role: "Baseline" },
];

function TranslationCondition({ condition, status, result, loading, copied, onCopy }) {
  return <article className={`comparison-result ${condition.key}`}>
    <div className="condition-header">
      <div><span className="condition-role">{condition.role}</span><h2>{condition.label}</h2></div>
      <span className={`translation-status ${status?.ready ? "ready" : "waiting"}`}>
        <span className="translation-status-dot" aria-hidden="true" />
        {status?.ready ? "Ready" : "Unavailable"}
      </span>
    </div>
    <div className="comparison-output" aria-live="polite">
      <div className="output-label-row"><span>Filipino output</span>
        {result?.translation && <button className="inline-copy-button" onClick={onCopy} aria-label={`Copy ${condition.short} translation`}>
          <CopyIcon />{copied ? "Copied" : "Copy"}
        </button>}
      </div>
      <p className={result ? "translation-text" : "comparison-placeholder"}>
        {loading ? "Generating translation..." : result ? result.translation || "No visible text was generated." : status?.ready ? "Compare a sentence to see the translation here." : status?.reason || "Checking model availability..."}
      </p>
    </div>
    <div className="translation-metrics" aria-label={`${condition.short} generation metrics`}>
      <div><span>Source tokens</span><strong>{result?.source_token_count ?? "Pending"}</strong></div>
      <div><span>Output tokens</span><strong>{result?.output_token_count ?? "Pending"}</strong></div>
      <div><span>Generation time</span><strong>{result?.cache_hit ? "Cached" : result ? `${result.latency_ms} ms` : "Pending"}</strong></div>
    </div>
  </article>;
}

export default function TranslatorComparisonPage() {
  const [source, setSource] = useState("");
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statusLoading, setStatusLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(null);
  const [processKey, setProcessKey] = useState("custom");

  async function checkStatus() {
    setStatusLoading(true); setError(null);
    try { setStatus(await getTranslationStatus()); }
    catch { setStatus(null); setError("Could not reach the translation backend. Start the backend, then check the connection."); }
    finally { setStatusLoading(false); }
  }
  useEffect(() => { checkStatus(); }, []);

  const canTranslate = Boolean(status?.can_translate);
  async function runComparison() {
    if (loading || statusLoading || !source.trim() || !canTranslate) return;
    setLoading(true); setError(null); setResult(null); setCopied(null);
    try {
      const data = await compareTranslations(source.trim());
      setResult(data);
      setProcessKey(data.custom ? "custom" : "baseline");
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  }
  function clear() { setSource(""); setResult(null); setError(null); setCopied(null); }
  async function copy(key) {
    try { await navigator.clipboard.writeText(result[key].translation); setCopied(key); }
    catch { setError("Clipboard access is unavailable. Select and copy the translation manually."); }
  }
  const active = CONDITIONS.find(condition => condition.key === processKey);

  return <main className="page translation-comparison-page">
    <div className="comparison-kicker">Controlled A/B comparison</div>
    <h1 className="page-title">Translator vs. Translator</h1>
    <p className="page-subtitle translation-comparison-subtitle">One Kapampangan input, two NLLB-200 conditions. Compare their Filipino output and follow how each translation is produced.</p>

    {error && <div className="error-banner" role="alert">{error}</div>}
    <div className="translation-test-grid">
      <section className="card text-panel comparison-input" aria-labelledby="comparison-input-label">
        <label className="card-pill" id="comparison-input-label" htmlFor="comparison-source">Kapampangan</label>
        <span className="source-step">Shared input</span>
        <textarea id="comparison-source" value={source} maxLength={MAX_LEN} disabled={loading}
          placeholder="Enter the same Kapampangan sentence for both translators..."
          onChange={event => { setSource(event.target.value); setResult(null); setCopied(null); }}
          onKeyDown={event => {
            if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) { event.preventDefault(); runComparison(); }
          }} />
        <p className="comparison-input-note">Each condition uses its own 6,080-token source vocabulary and trained source embeddings. Both use the same frozen NLLB base and decoding settings.</p>
        <div className="panel-footer">
          <div className="button-row">
            <button className="btn btn-primary" onClick={runComparison} disabled={!source.trim() || !canTranslate || loading || statusLoading}>
              <CompareIcon className="btn-icon" />
              {statusLoading ? "Checking models..." : loading ? "Translating..." : status?.can_compare ? "Compare translations" : "Translate available model"}
            </button>
            <button className="btn btn-secondary" onClick={clear} disabled={loading}><TrashIcon className="btn-icon" />Clear</button>
          </div>
          <span className="char-count">{source.length}/{MAX_LEN}</span>
        </div>
      </section>
      <section className="card comparison-results" aria-labelledby="comparison-results-label" aria-busy={loading}>
        <span className="card-pill" id="comparison-results-label">Results</span>
        {CONDITIONS.map(condition => <TranslationCondition key={condition.key} condition={condition}
          status={status?.conditions?.[condition.key]} result={result?.[condition.key]} loading={loading && status?.conditions?.[condition.key]?.ready}
          copied={copied === condition.key} onCopy={() => copy(condition.key)} />)}
        <p className="comparison-results-note">Source counts include start/end tokens. Output counts exclude special tokens. These are generation statistics, not translation-quality scores.</p>
      </section>
    </div>
    {loading && <p className="translator-note" role="status">Loading or translating. The first request may load the base model. Both results appear when the comparison finishes.</p>}
    {!status?.can_compare && !statusLoading && <aside className="readiness-callout">
      <div><strong>Translation availability</strong><p>{status?.message || "Start the backend and check the connection."}</p></div>
      <button className="btn btn-secondary" onClick={checkStatus} disabled={loading}>Check connection</button>
    </aside>}

    <div className="process-switch" role="group" aria-label="Translation process condition">
      <span>Explain the process for</span>
      {CONDITIONS.map(condition => <button key={condition.key} className={`example-chip ${processKey === condition.key ? "selected" : ""}`}
        aria-pressed={processKey === condition.key} onClick={() => setProcessKey(condition.key)}>{condition.short}</button>)}
    </div>
    <TranslationProcess result={result?.[processKey]} label={active.short} />
  </main>;
}
