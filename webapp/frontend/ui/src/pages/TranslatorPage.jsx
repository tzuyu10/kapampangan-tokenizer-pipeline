import { useEffect, useState } from "react";
import { getTranslationStatus, translateAdapted, tokenizeAdapted } from "../api.js";

export default function TranslatorPage() {
  const [condition, setCondition] = useState("plain_bpe");
  const [tokens, setTokens] = useState(null);
  const label = condition === "plain_bpe" ? "Plain BPE" : "Morph-BPE";
  const [source, setSource] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [checking, setChecking] = useState(true);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const ready = Boolean(status?.conditions?.[condition === "plain_bpe" ? "baseline" : "custom"]?.ready);
  async function checkStatus() {
    setChecking(true); setError("");
    try { setStatus(await getTranslationStatus()); }
    catch { setStatus(null); setError("Cannot reach the backend. Start webapp/start-translation-backend.cmd, then click Check connection."); }
    finally { setChecking(false); }
  }
  useEffect(() => { checkStatus(); }, []);
  async function run() {
    if (loading || !ready || !source.trim()) return;
    setLoading(true); setError(""); setResult(null); setCopied(false);
    try { setResult(await translateAdapted(source.trim(), condition)); }
    catch (e) { setError(e.message.includes("fetch") ? "Connection lost. Check the backend terminal, then retry." : e.message); }
    finally { setLoading(false); }
  }
  async function copy() {
    try { await navigator.clipboard.writeText(result.translation); setCopied(true); }
    catch { setError("Clipboard unavailable. Select and copy the translation manually."); }
  }
  return <main className="page">
    <h1 className="page-title">Kapampangan-Filipino Translator</h1>
    <p className="page-subtitle">Adapted Plain BPE and Morph-BPE + NLLB-200 600M</p>
    <label className="model-selector">Model and tokenizer <select aria-label="Model and tokenizer" disabled={loading} value={condition} onChange={e => {setCondition(e.target.value);setResult(null);setTokens(null);setError("");}}><option value="plain_bpe">Plain BPE</option><option value="morph_bpe">Morph-BPE</option></select></label>
    <div className="plainbpe-status" role="status">
      <span>{checking ? "Checking backend..." : ready ? `${label} checkpoint available` : `${label} unavailable`}</span>
      <button className="btn btn-secondary" disabled={checking || loading} onClick={checkStatus}>Check connection</button>
    </div>
    {!checking && status && !ready && <p>{status.conditions?.[condition === "plain_bpe" ? "baseline" : "custom"]?.reason}</p>}
    {error && <div className="error-banner" role="alert">{error}</div>}
    <div className="plainbpe-panels">
      <div className="card text-panel">
        <label className="card-pill" htmlFor="plainbpe-source">Kapampangan</label>
        <textarea id="plainbpe-source" value={source} maxLength={500} disabled={loading}
          onChange={e => { setSource(e.target.value); setTokens(null); setResult(null); setCopied(false); }}
          onKeyDown={e => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); run(); } }}
          placeholder="Enter Kapampangan text" />
        <div className="panel-footer">
          <div className="button-row">
            <button className="btn btn-primary" disabled={loading || checking || !ready || !source.trim()} onClick={run}>{loading ? 'Translating...' : `Translate with ${label}`}</button>
            <button className="btn btn-secondary" disabled={loading} onClick={() => { setSource(''); setTokens(null); setResult(null); setError(''); setCopied(false); }}>Clear</button>
          </div>
          <span className="char-count">{source.length}/500</span>
        </div>
      </div>
      <div className="card text-panel" aria-busy={loading}>
        <label className="card-pill" htmlFor="plainbpe-output">Filipino</label>
        <textarea id="plainbpe-output" readOnly value={result?.translation || ''} placeholder={loading ? 'Generating your translation...' : 'Translation appears here'} />
        <div className="panel-footer"><button className="btn btn-secondary" disabled={!result?.translation} onClick={copy}>{copied ? 'Copied' : 'Copy translation'}</button></div>
      </div>
    </div>
    {loading && <p role="status">Loading or translating. The first request may download the base model; check the backend terminal for progress.</p>}
    {result && <p className="translator-note">{label} output · {result.source_token_count} source tokens · {result.output_token_count} output tokens · {result.cache_hit ? 'Cached translation' : `${result.latency_ms} ms generation time`}</p>}
    <div className="translator-token-actions">
    <button className="btn btn-secondary" disabled={loading || !source.trim()} onClick={async () => {
      setError(''); setTokens(null); setLoading(true);
      try { setTokens(await tokenizeAdapted(source, condition)); } catch(e) {setError(e.message);} finally {setLoading(false);}
    }}>Show {label} tokens</button>
    </div>
    {tokens && <section className="card translator-token-result"><h2>{label} tokenization</h2>
      <p>{tokens.tokens.map((t,i) => <code key={i} style={{display:'inline-block',whiteSpace:'pre-wrap',padding:'6px',margin:'3px',border:'1px solid #bbb'}}>{t.token}</code>)}</p>
      <p className="process-body">Token IDs: {tokens.ids.join(', ')}</p>
      <details><summary>Model input IDs (including boundary tokens)</summary><p style={{overflowWrap:'anywhere'}}>{tokens.model_source_ids.join(', ')}</p></details>
    </section>}
    <p className="translator-note">Tokenization uses the exact artifact from the selected trained model.</p>
  </main>;
}
