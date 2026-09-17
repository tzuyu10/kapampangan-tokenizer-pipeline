import { useEffect, useState } from "react";
import { CompareIcon, CopyIcon, TrashIcon } from "../components/icons.jsx";
import { compareTranslations, getTranslationStatus } from "../api.js";

const MAX_LEN = 500;

const DEMO_INPUT = "Masanting ya ing abak. Komusta ka?";

const DEMO_RESULT = {
  custom: {
    translation: "Magandang umaga. Kumusta ka?",
    source_token_count: 11,
    output_token_count: 9,
    latency_ms: 684,
  },
  baseline: {
    translation: "Magandang umaga po. Kamusta ka?",
    source_token_count: 17,
    output_token_count: 11,
    latency_ms: 731,
  },
};

const FALLBACK_CONDITIONS = {
  custom: {
    label: "MorphBPE + NLLB-200",
    role: "Proposed system",
    tokenizer: "MorphBPE penalty-32 (6,080 source tokens)",
    model: "NLLB-200 Distilled 600M with source embedding swap",
    ready: false,
    reason: "The custom-tokenizer translation checkpoint is not available.",
  },
  baseline: {
    label: "Original NLLB-200",
    role: "Baseline",
    tokenizer: "Native NLLB-200 tokenizer",
    model: "facebook/nllb-200-distilled-600M",
    ready: false,
    reason: "The original NLLB-200 model is not available.",
  },
};

function StatusBadge({ ready, demo }) {
  return (
    <span className={`translation-status ${demo ? "demo" : ready ? "ready" : "waiting"}`}>
      <span className="translation-status-dot" aria-hidden="true" />
      {demo ? "Demo data" : ready ? "Ready" : "Checkpoint required"}
    </span>
  );
}

function TranslationCondition({ condition, result, copied, onCopy, accent, demo }) {
  const translation = result?.translation || "";

  return (
    <article className={`translation-condition ${accent}`}>
      <div className="condition-header">
        <div>
          <span className="condition-role">{condition.role}</span>
          <h2>{condition.label}</h2>
        </div>
        <StatusBadge ready={condition.ready} demo={demo} />
      </div>

      <dl className="condition-specs">
        <div>
          <dt>Source tokenizer</dt>
          <dd>{condition.tokenizer}</dd>
        </div>
        <div>
          <dt>Translation model</dt>
          <dd>{condition.model}</dd>
        </div>
      </dl>

      <div className={`translation-output ${translation ? "has-result" : ""}`}>
        <div className="output-label-row">
          <span>Filipino output</span>
          {translation && (
            <button
              className="inline-copy-button"
              type="button"
              onClick={onCopy}
              aria-label={`Copy ${condition.label} translation`}
            >
              <CopyIcon />
              {copied ? "Copied" : "Copy"}
            </button>
          )}
        </div>
        {translation ? (
          <p className="translation-text">{translation}</p>
        ) : (
          <div className="output-empty">
            <span className="output-empty-mark" aria-hidden="true">Aa</span>
            <p>{condition.reason}</p>
          </div>
        )}
      </div>

      <div className="translation-metrics" aria-label={`${condition.label} generation metrics`}>
        <div>
          <span>Source tokens</span>
          <strong>{result?.source_token_count ?? "—"}</strong>
        </div>
        <div>
          <span>Output tokens</span>
          <strong>{result?.output_token_count ?? "—"}</strong>
        </div>
        <div>
          <span>Latency</span>
          <strong>{result?.latency_ms != null ? `${result.latency_ms} ms` : "—"}</strong>
        </div>
      </div>
    </article>
  );
}

export default function TranslatorComparisonPage() {
  const [source, setSource] = useState("");
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statusLoading, setStatusLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(null);
  const [isDemo, setIsDemo] = useState(false);

  useEffect(() => {
    getTranslationStatus()
      .then(setStatus)
      .catch(() => {
        setError("Could not reach the translation backend on port 8000.");
      })
      .finally(() => setStatusLoading(false));
  }, []);

  const conditions = status?.conditions || FALLBACK_CONDITIONS;
  const canCompare = Boolean(status?.can_compare);

  const runComparison = async () => {
    if (!source.trim() || !canCompare) return;
    setLoading(true);
    setError(null);
    setIsDemo(false);
    try {
      setResult(await compareTranslations(source.trim()));
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const clear = () => {
    setSource("");
    setResult(null);
    setError(null);
    setIsDemo(false);
  };

  const loadDemo = () => {
    setSource(DEMO_INPUT);
    setResult(DEMO_RESULT);
    setError(null);
    setCopied(null);
    setIsDemo(true);
  };

  const copy = async (key) => {
    const value = result?.[key]?.translation;
    if (!value) return;
    try {
      await navigator.clipboard.writeText(value);
      setCopied(key);
      window.setTimeout(() => setCopied(null), 1200);
    } catch {
      setError("Clipboard access is unavailable in this browser.");
    }
  };

  const buttonLabel = statusLoading
    ? "Checking models…"
    : loading
      ? "Comparing…"
      : canCompare
        ? "Compare translations"
        : "Models not ready";

  return (
    <main className="page translation-comparison-page">
      <div className="comparison-kicker">Controlled A/B comparison</div>
      <h1 className="page-title">Translator vs. Translator</h1>
      <p className="page-subtitle translation-comparison-subtitle">
        One Kapampangan input, two NLLB-200 conditions. The only intended difference is
        the source tokenizer and its matching encoder embedding.
      </p>

      {error && <div className="error-banner">{error}</div>}
      {isDemo && (
        <div className="demo-data-banner" role="status">
          <strong>Demo preview</strong>
          <span>
            These translations and measurements are dummy data for interface testing, not
            model-generated results.
          </span>
        </div>
      )}

      <section className="translation-source-card" aria-labelledby="source-heading">
        <div className="source-card-heading">
          <div>
            <span className="source-step">01 · Shared input</span>
            <h2 id="source-heading">Kapampangan source text</h2>
          </div>
          <span className="direction-chip">Kapampangan <b>→</b> Filipino</span>
        </div>
        <label className="sr-only" htmlFor="comparison-source">Kapampangan source text</label>
        <textarea
          id="comparison-source"
          value={source}
          maxLength={MAX_LEN}
          placeholder="Enter the same Kapampangan sentence for both translators…"
          onChange={(event) => {
            setSource(event.target.value);
            if (isDemo) {
              setResult(null);
              setIsDemo(false);
            }
          }}
          onKeyDown={(event) => {
            if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) runComparison();
          }}
        />
        <div className="source-actions">
          <div className="button-row">
            <button
              className="btn btn-primary compare-translation-button"
              type="button"
              onClick={runComparison}
              disabled={!source.trim() || !canCompare || loading || statusLoading}
            >
              <CompareIcon className="btn-icon" />
              {buttonLabel}
            </button>
            <button className="btn btn-secondary" type="button" onClick={clear}>
              <TrashIcon className="btn-icon" />
              Clear
            </button>
            <button className="btn btn-demo" type="button" onClick={loadDemo}>
              Load demo data
            </button>
          </div>
          <span className="char-count">{source.length}/{MAX_LEN}</span>
        </div>
      </section>

      <div className="results-heading-row">
        <div>
          <span className="source-step">02 · Side-by-side output</span>
          <h2>Compare the translations</h2>
        </div>
        <p>Same decoding settings · Filipino target · No post-editing</p>
      </div>

      <section className="translator-versus-grid">
        <TranslationCondition
          condition={conditions.custom}
          result={result?.custom}
          copied={copied === "custom"}
          onCopy={() => copy("custom")}
          accent="custom"
          demo={isDemo}
        />
        <div className="versus-marker" aria-hidden="true">VS</div>
        <TranslationCondition
          condition={conditions.baseline}
          result={result?.baseline}
          copied={copied === "baseline"}
          onCopy={() => copy("baseline")}
          accent="baseline"
          demo={isDemo}
        />
      </section>

      {!canCompare && !statusLoading && !isDemo && (
        <aside className="readiness-callout">
          <div className="readiness-icon" aria-hidden="true">i</div>
          <div>
            <strong>Interface ready; model inference pending</strong>
            <p>
              {status?.message || "The required translation checkpoints are not available."}
              {" "}This screen intentionally shows no generated text until both real model
              conditions can run.
            </p>
          </div>
        </aside>
      )}
    </main>
  );
}
