const NAMES = ["MorphBPE", "Plain BPE", "Unigram-LM"];
const DOT_CLASS = { MorphBPE: "morph", "Plain BPE": "plain", "Unigram-LM": "uni" };

function TokLabel({ name }) {
  return (
    <span>
      <span className={`tok-dot ${DOT_CLASS[name]}`} />
      {name}
    </span>
  );
}

function fmt(n, digits = 3) {
  if (n === null || n === undefined) return "—";
  return n.toFixed(digits);
}

function BarRow({ name, value, max, formatted }) {
  const pct = max > 0 ? Math.max(2, Math.min(100, (value / max) * 100)) : 0;
  return (
    <div className="metric-bar-row">
      <span className="metric-bar-label">
        <TokLabel name={name} />
      </span>
      <div className="metric-bar-track">
        <div className={`metric-bar-fill ${DOT_CLASS[name]}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="metric-bar-value">{formatted}</span>
    </div>
  );
}

function MetricChart({ title, note, values, digits = 3, scaleMax }) {
  const max = scaleMax ?? Math.max(1, ...NAMES.map((n) => values[n] ?? 0)) * 1.15;
  return (
    <div className="metric-chart">
      <p className="metric-chart-title">{title}</p>
      {note && <p className="metric-chart-note">{note}</p>}
      <div className="metric-bar-rows">
        {NAMES.map((n) => (
          <BarRow key={n} name={n} value={values[n] ?? 0} max={max} formatted={fmt(values[n], digits)} />
        ))}
      </div>
    </div>
  );
}

function SplitsSection({ result }) {
  return (
    <div className="comparison-section">
      <h2 className="comparison-section-title">Your Input — 3-Way Split</h2>
      <p className="comparison-section-note">
        The same text you tokenized on the Tokenizer tab (<code>{result.input}</code>), run
        through all three tokenizers live. &ldquo;+&rdquo; marks a subword join.
      </p>
      <div className="card" style={{ padding: "20px 24px" }}>
        {NAMES.map((n) => (
          <p key={n} style={{ margin: "8px 0", fontSize: 15 }}>
            <TokLabel name={n} />{" "}
            {result.splits[n].map((g) => g.join("+")).join("  |  ")}
          </p>
        ))}
      </div>
    </div>
  );
}

function FertilityExplain({ fertility }) {
  return (
    <details className="compute-block">
      <summary>How Fertility is computed</summary>
      <p className="compute-note">
        From <code>comparison_service.custom_compare()</code>: fertility = tokens produced ÷
        number of words. No gold data needed.
      </p>
      {NAMES.map((n) => {
        const f = fertility[n];
        return (
          <p key={n} className="compute-line">
            <TokLabel name={n} /> — {f.tokens} tokens ÷ {f.words} word{f.words === 1 ? "" : "s"} ={" "}
            <b>{fmt(f.score)}</b>
          </p>
        );
      })}
    </details>
  );
}

function BoundaryExplainTokenizer({ name, explain }) {
  return (
    <div className="compute-tokenizer-block">
      <p className="compute-tokenizer-title">
        <TokLabel name={name} />
      </p>
      <div className="table-scroll">
        <table className="comparison-table compute-table">
          <thead>
            <tr>
              <th>Word</th>
              <th>Gold pieces</th>
              <th>Predicted pieces</th>
              <th>Gold cuts</th>
              <th>Predicted cuts</th>
              <th>Match / Extra / Missed</th>
            </tr>
          </thead>
          <tbody>
            {explain.per_word.map((w, i) => (
              <tr key={`${w.surface}-${i}`}>
                <td>{w.surface}</td>
                <td>{w.gold_pieces.join(" · ")}</td>
                <td>{w.pred_pieces.join(" · ")}</td>
                <td>{w.gold_boundaries.join(", ") || "—"}</td>
                <td>{w.pred_boundaries.join(", ") || "—"}</td>
                <td>
                  {w.tp_boundaries.length} match / {w.fp_boundaries.length} extra /{" "}
                  {w.fn_boundaries.length} missed
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="compute-line">
        Totals across all words — TP = {explain.tp}, FP = {explain.fp}, FN = {explain.fn}
      </p>
      <p className="compute-line">
        precision = TP/(TP+FP) = {explain.tp}/({explain.tp}+{explain.fp}) ={" "}
        <b>{fmt(explain.precision)}</b>
      </p>
      <p className="compute-line">
        recall = TP/(TP+FN) = {explain.tp}/({explain.tp}+{explain.fn}) = <b>{fmt(explain.recall)}</b>
      </p>
      <p className="compute-line">
        F1 = 2·precision·recall/(precision+recall) = <b>{fmt(explain.f1)}</b>
      </p>
    </div>
  );
}

function BoundaryExplain({ explain }) {
  return (
    <details className="compute-block">
      <summary>How Boundary F1 is computed</summary>
      <p className="compute-note">
        From <code>reference_data.py</code>'s <code>score()</code>: each tokenizer's produced
        pieces are turned into cut positions (the running character offset after every piece
        except the last), pooled across all words, and compared against the cut positions your{" "}
        <code>|</code> marks specify.
      </p>
      {NAMES.map((n) => (
        <BoundaryExplainTokenizer key={n} name={n} explain={explain[n].boundary} />
      ))}
    </details>
  );
}

function ConsistencyExplainTokenizer({ name, explain }) {
  const groupText = (groups, keyName) =>
    groups.length === 0
      ? "none"
      : groups.map((g) => `'${g[keyName]}' → ${g.words.join(", ")}`).join("; ");
  const pairText = (pairs) => (pairs.length ? ` [${pairs.map((p) => p.join(" ↔ ")).join(", ")}]` : "");

  return (
    <div className="compute-tokenizer-block">
      <p className="compute-tokenizer-title">
        <TokLabel name={name} />
      </p>
      <p className="compute-line">
        Shared-morpheme groups (gold, length ≥2): {groupText(explain.morpheme_groups, "morpheme")}
      </p>
      <p className="compute-line">
        Shared-token groups (this tokenizer's output, length ≥2):{" "}
        {groupText(explain.token_groups, "token")}
      </p>
      <p className="compute-line">
        matched pairs (TP) = {explain.tp}
        {pairText(explain.tp_pairs)}
      </p>
      <p className="compute-line">
        missed pairs (FN) = {explain.fn}
        {pairText(explain.fn_pairs)}
      </p>
      <p className="compute-line">
        extra pairs (FP) = {explain.fp}
        {pairText(explain.fp_pairs)}
      </p>
      <p className="compute-line">
        precision = TP/(TP+FP) = <b>{fmt(explain.precision)}</b>
      </p>
      <p className="compute-line">
        recall = TP/(TP+FN) = <b>{fmt(explain.recall)}</b>
      </p>
      <p className="compute-line">
        F1 = 2·precision·recall/(precision+recall) = <b>{fmt(explain.f1)}</b>
      </p>
    </div>
  );
}

function ConsistencyExplain({ explain }) {
  return (
    <details className="compute-block">
      <summary>How Consistency F1 (MCF1) is computed</summary>
      <p className="compute-note">
        From <code>reference_data.py</code>'s <code>mcf1()</code>: words are grouped by any
        shared gold morpheme, and separately by any shared produced token (each ≥2 characters);
        every pair of words within a group of 2+ counts once. A pair is a true positive only if
        it shares both a gold morpheme <em>and</em> a token.
      </p>
      {NAMES.map((n) => (
        <ConsistencyExplainTokenizer key={n} name={n} explain={explain[n].consistency} />
      ))}
    </details>
  );
}

export default function ComparisonPage({ input, result, loading, error, onGoToTokenizer }) {
  return (
    <div className="page">
      <h1 className="page-title">Tokenizer Comparison</h1>
      <p className="page-subtitle">
        MorphBPE penalty-32 vs. Plain BPE vs. Unigram-LM (NLLB&rsquo;s own algorithm) — using the
        same input you tokenize on the Tokenizer tab
      </p>

      {error && <div className="error-banner">{error}</div>}

      {!input && !loading && !error && (
        <div className="card comparison-empty-card">
          <p>
            Type something in the <b>Tokenizer</b> tab and press <b>Tokenize</b> — the exact same
            input is compared here across all three tokenizers, live.
          </p>
          <button className="btn btn-primary" onClick={onGoToTokenizer}>
            Go to Tokenizer tab
          </button>
        </div>
      )}

      {loading && <p style={{ textAlign: "center", color: "#9a9a9a" }}>Comparing…</p>}

      {result && (
        <>
          <SplitsSection result={result} />

          <div className="comparison-section">
            <h2 className="comparison-section-title">Score Comparison</h2>
            <p className="comparison-section-note">
              Every score below is computed live from the actual artifacts for the exact text you
              tokenized — nothing here is pre-baked.
            </p>
            <div className="metric-chart-grid">
              <MetricChart
                title="1.1 Fertility (pieces / word)"
                note="lower = tighter segmentation"
                values={Object.fromEntries(NAMES.map((n) => [n, result.fertility[n].score]))}
              />
              {result.gold ? (
                <>
                  <MetricChart
                    title="1.2 Boundary F1"
                    note="cuts landing on a gold morpheme boundary"
                    values={Object.fromEntries(
                      NAMES.map((n) => [n, result.gold.metrics[n].boundary_f1])
                    )}
                    scaleMax={1}
                  />
                  {result.gold.shared_pairs > 0 ? (
                    <MetricChart
                      title="1.3 Consistency F1"
                      note="a morpheme shared by two words, cut alike"
                      values={Object.fromEntries(
                        NAMES.map((n) => [n, result.gold.metrics[n].mcf1])
                      )}
                      scaleMax={1}
                    />
                  ) : (
                    <div className="card metric-chart-hint">
                      <p>
                        No two words in this input share a gold morpheme, so Consistency F1 isn&rsquo;t
                        meaningful here — try marking two related word forms, e.g.{" "}
                        <code>ka|ligtas|an mag|ligtas</code>.
                      </p>
                    </div>
                  )}
                </>
              ) : (
                <div className="card metric-chart-hint">
                  <p>
                    Mark gold boundaries with <code>|</code> in the Tokenizer tab (e.g.{" "}
                    <code>s|in|ulat</code>) to also compare Boundary F1 and Consistency F1 here.
                  </p>
                </div>
              )}
            </div>
          </div>

          <div className="comparison-section">
            <h2 className="comparison-section-title">How These Scores Are Computed</h2>
            <p className="comparison-section-note">
              Straight from the scoring code — the numbers below are the exact intermediate
              values used to produce the scores above, verified at server startup to match{" "}
              <code>reference_data.py</code> exactly.
            </p>
            <FertilityExplain fertility={result.fertility} />
            {result.gold && <BoundaryExplain explain={result.gold.explain} />}
            {result.gold && <ConsistencyExplain explain={result.gold.explain} />}
          </div>
        </>
      )}
    </div>
  );
}
