import { useEffect, useState } from "react";
import { TrashIcon } from "../components/icons.jsx";
import ResultsPanel from "../components/ResultsPanel.jsx";
import SegmentationProcess from "../components/SegmentationProcess.jsx";
import ExampleChips from "../components/ExampleChips.jsx";
import { tokenize, getExamples } from "../api.js";

const MAX_LEN = 500;

export default function TokenizerPage({ onTokenized, onCleared }) {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [examples, setExamples] = useState(null);

  useEffect(() => {
    getExamples()
      .then(setExamples)
      .catch(() => setExamples(null)); // backend not running yet — chips just won't show
  }, []);

  const runTokenize = async (value) => {
    const target = value !== undefined ? value : text;
    if (!target.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await tokenize(target);
      setResult(data);
      onTokenized?.(target);
    } catch (err) {
      setError(
        err.message.includes("fetch")
          ? "Could not reach the tokenizer backend. Is `python server.py` running on port 8000?"
          : err.message
      );
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setText("");
    setResult(null);
    setError(null);
    onCleared?.();
  };

  const handleExamplePick = (value) => {
    setText(value);
    runTokenize(value);
  };

  return (
    <div className="page">
      <h1 className="page-title">Kapampangan Tokenizer</h1>
      <p className="page-subtitle">
        Powered by Morphologically-Aware Byte-Pair Encoding Tokenizer for the Kapampangan
        Language
      </p>

      {error && <div className="error-banner">{error}</div>}

      <div className="two-column tokenizer-columns">
        <div className="card text-panel">
          <span className="card-pill">Kapampangan</span>
          <textarea
            placeholder="Enter text here"
            maxLength={MAX_LEN}
            value={text}
            onChange={(e) => setText(e.target.value)}
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
                disabled={loading || !text.trim()}
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
      <SegmentationProcess result={result} />
    </div>
  );
}
