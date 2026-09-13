function fmt(n) {
  return n.toFixed(3).replace(/0+$/, "").replace(/\.$/, ".0");
}

function StatBlock({ label, value, sub, muted }) {
  return (
    <div>
      <p className="result-stat-label">{label}</p>
      <p className={`result-stat-value ${muted ? "muted" : ""}`}>{value}</p>
      {sub && <p className="result-stat-sub">{sub}</p>}
    </div>
  );
}

export default function ResultsPanel({ result }) {
  if (!result || !result.fertility) {
    return (
      <div className="card results-panel">
        <span className="card-pill">Results</span>
        <StatBlock label="Fertility Score" value="—" sub="pieces produced per word" muted />
        <StatBlock label="Boundary F1" value="—" sub="how many cuts land on a real morpheme seam" muted />
        <StatBlock label="Consistency F1" value="—" sub="is a shared morpheme cut the same way twice?" muted />
      </div>
    );
  }

  const { fertility, gold } = result;

  return (
    <div className="card results-panel">
      <span className="card-pill">Results</span>

      <StatBlock
        label="Fertility Score"
        value={fmt(fertility.score)}
        sub={`${fertility.tokens} tokens across ${fertility.words} word${fertility.words === 1 ? "" : "s"}`}
      />

      {gold ? (
        <StatBlock
          label="Boundary F1"
          value={fmt(gold.boundary_f1)}
          sub={`precision ${fmt(gold.boundary_precision)} · recall ${fmt(gold.boundary_recall)}`}
        />
      ) : (
        <StatBlock
          label="Boundary F1"
          value="N/A"
          sub="mark gold boundaries with | to compute (e.g. s|in|ulat)"
          muted
        />
      )}

      {gold && gold.consistency_f1 !== null ? (
        <StatBlock
          label="Consistency F1"
          value={fmt(gold.consistency_f1)}
          sub={`${gold.shared_morpheme_pairs} shared-morpheme pair${gold.shared_morpheme_pairs === 1 ? "" : "s"}`}
        />
      ) : (
        <StatBlock
          label="Consistency F1"
          value="N/A"
          sub={gold ? "no two marked words share a morpheme here" : "needs | boundaries on 2+ related words"}
          muted
        />
      )}
    </div>
  );
}
