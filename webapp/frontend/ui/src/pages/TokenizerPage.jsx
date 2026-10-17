import { useCallback, useEffect, useRef, useState } from "react";
import { TrashIcon } from "../components/icons.jsx";
import ResultsPanel from "../components/ResultsPanel.jsx";
import SegmentationProcess from "../components/SegmentationProcess.jsx";
import ExampleChips from "../components/ExampleChips.jsx";
import { tokenize, getExamples, getTokenizers } from "../api.js";

const MAX_LEN = 500;
const DEFAULT_TOKENIZER = "variant:pam_tl_infix_first48_6080";

export default function TokenizerPage({ translationSource, onTokenized, onCleared }) {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [examples, setExamples] = useState(null);
  const [tokenizers, setTokenizers] = useState([]);
  const [selectedTokenizer, setSelectedTokenizer] = useState(DEFAULT_TOKENIZER);
  const [catalogLoading, setCatalogLoading] = useState(true);
  const [catalogError, setCatalogError] = useState(null);
  const tokenizationRequest = useRef(0);
  const catalogRequest = useRef(0);

  const resetTokenization = useCallback(() => {
    tokenizationRequest.current += 1;
    setResult(null);
    setError(null);
    setLoading(false);
    onCleared?.();
  }, [onCleared]);

  const loadTokenizers = useCallback(async () => {
    const request = ++catalogRequest.current;
    resetTokenization();
    setCatalogLoading(true);
    setCatalogError(null);
    try {
      const catalog = await getTokenizers();
      if (request !== catalogRequest.current) return;
      const available = catalog.tokenizers || [];
      if (!available.length) throw new Error("No tokenizer variants are available. Check the backend artifacts, then retry.");
      setTokenizers(available);
      setSelectedTokenizer(current => available.some(item => item.id === current) ? current
        : available.some(item => item.id === catalog.default_tokenizer) ? catalog.default_tokenizer : available[0].id);
    } catch (err) {
      if (request !== catalogRequest.current) return;
      setTokenizers([]);
      setCatalogError(err.message.includes("fetch")
        ? "Could not load tokenizer variants. Start the backend, then retry."
        : err.message);
    } finally {
      if (request === catalogRequest.current) setCatalogLoading(false);
    }
  }, [resetTokenization]);

  useEffect(() => {
    loadTokenizers();
    return () => { catalogRequest.current += 1; tokenizationRequest.current += 1; };
  }, [loadTokenizers]);

  useEffect(() => {
    setText(translationSource);
    resetTokenization();
  }, [translationSource, resetTokenization]);

  useEffect(() => {
    getExamples()
      .then(setExamples)
      .catch(() => setExamples(null)); // Examples are optional while the backend is unavailable.
  }, []);

  const runTokenize = async (value) => {
    const target = value !== undefined ? value : text;
    if (!target.trim() || catalogLoading || !tokenizers.some(item => item.id === selectedTokenizer)) return;
    const request = ++tokenizationRequest.current;
    setLoading(true);
    setError(null);
    try {
      const data = await tokenize(target, selectedTokenizer);
      if (request !== tokenizationRequest.current) return;
      setResult(data);
      onTokenized?.(target, selectedTokenizer);
    } catch (err) {
      if (request !== tokenizationRequest.current) return;
      setError(
        err.message.includes("fetch")
          ? "Could not reach the tokenizer backend. Is `python server.py` running on port 8000?"
          : err.message
      );
      setResult(null);
    } finally {
      if (request === tokenizationRequest.current) setLoading(false);
    }
  };

  const handleClear = () => {
    setText("");
    resetTokenization();
  };

  const handleExamplePick = (value) => {
    resetTokenization();
    setText(value);
    runTokenize(value);
  };

  const selectedMetadata = tokenizers.find(item => item.id === selectedTokenizer);
  const selectedName = selectedMetadata?.label || "Selected tokenizer";
  const resultName = result?.tokenizer?.label || selectedName;
  const vocabularySize = selectedMetadata?.vsize ?? selectedMetadata?.source_vocab_size;

  return (
    <div className="page">
      <h1 className="page-title">Tokenizer Process Visualization</h1>
      <p className="page-subtitle">
        Kapampangan input → selected tokenizer output → step-by-step segmentation.
      </p>

      <label>Tokenizer variant <select value={selectedTokenizer} disabled={catalogLoading || !tokenizers.length}
        onChange={event => { setSelectedTokenizer(event.target.value); resetTokenization(); }}>
        {catalogLoading ? <option value={selectedTokenizer}>Loading tokenizer variants...</option>
          : !tokenizers.length ? <option value={selectedTokenizer}>No tokenizer variants available</option>
          : tokenizers.map(item => <option key={item.id} value={item.id}>{item.label || item.id}</option>)}
      </select></label>
      {catalogError && <p role="alert">{catalogError} <button className="example-chip" onClick={loadTokenizers}>Retry</button></p>}
      {selectedMetadata && <p className="translator-note">Active tokenizer: {selectedName}
        {Number.isFinite(vocabularySize) && <> · {vocabularySize.toLocaleString()} source tokens</>}
        {selectedMetadata.source === "trained_bundle" ? " · From a trained model bundle" : " · Tokenizer artifact"}.
        {" "}This selection updates the tokenizer visualization and its matched comparison. Translation model selection is set when the backend starts.</p>}

      {error && <div className="error-banner">{error}</div>}
      {result?.gold_unavailable_reason && <p role="status">{result.gold_unavailable_reason}</p>}

      <div className="two-column tokenizer-columns">
        <div className="card text-panel">
          <span className="card-pill">Kapampangan</span>
          <textarea
            placeholder="Enter text here"
            maxLength={MAX_LEN}
            value={text}
            onChange={(e) => {
              setText(e.target.value);
              resetTokenization();
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) runTokenize();
            }}
          />
          <ExampleChips examples={examples} onPick={handleExamplePick} />
          <div className="panel-footer">
            <div className="button-row">
              <button
                className="btn btn-primary"
                onClick={() => runTokenize()}
                disabled={loading || catalogLoading || !tokenizers.length || !text.trim()}
              >
                {loading ? "Tokenizing…" : "Tokenize"}
              </button>
              <button className="btn btn-secondary" onClick={handleClear}>
                <TrashIcon className="btn-icon" />
                Clear
              </button>
            </div>
            <span className="char-count">
              {text.length}/{MAX_LEN}
            </span>
          </div>
        </div>

        <ResultsPanel result={result} />
      </div>

      <h2 className="segmentation-heading">Segmentation Process</h2>
      {result && <p className="translator-note">Segmentation shown for {resultName}.</p>}
      <SegmentationProcess result={result} />
    </div>
  );
}
