export default function ResultsPanel({ result }) {
  const tokens = result?.all_tokens || [];
  return <section className="card results-panel token-output-panel" aria-label="Tokenization output">
    <span className="card-pill">Token output</span>
    {result ? <>
      <p className="result-stat-label">Normalized input</p><p className="process-example">{result.normalized_text}</p>
      <p className="result-stat-label">Learned pieces</p><div className="token-output-pieces">{tokens.map((token, index) => <span className="token-output-chip" key={index} title={`Vocabulary ID ${token.id}`}>{token.token.replace(/\s/g, "␠")}</span>)}</div>
      <p className="process-hint">␠ marks whitespace. Hover over a piece to see its vocabulary ID.</p>
      <details><summary>Vocabulary IDs</summary><p className="process-id-list">{tokens.map(token => token.id).join(" · ")}</p></details>
      <p className="initial-metrics-note">Open Tokenization Comparison & Metrics for fertility and morphological scores.</p>
    </> : <p className="comparison-placeholder">Tokenize a Kapampangan sentence to see its learned pieces and vocabulary IDs.</p>}
  </section>;
}
