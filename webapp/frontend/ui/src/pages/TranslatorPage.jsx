import { useState } from "react";
import { TranslateIcon, TrashIcon, SwapIcon, CopyIcon } from "../components/icons.jsx";

const MAX_LEN = 500;

// NOTE: There is no trained Kapampangan<->Filipino translation model yet —
// the thesis pipeline currently ends at the tokenizer artifact (see the
// project's PAPER_TRACEABILITY / LIMITATIONS docs: NLLB fine-tuning is
// explicitly future work). This page is a UI shell only, matching the
// provided design, so the layout exists ahead of that model. It does not
// call the tokenizer backend at all.
export default function TranslatorPage() {
  const [source, setSource] = useState("");
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(source);
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    } catch {
      // clipboard API unavailable (e.g. non-HTTPS context) — fail silently
    }
  };

  return (
    <div className="page">
      <h1 className="page-title">Kapampangan-Filipino Translator</h1>
      <p className="page-subtitle">
        Powered by Morphologically-Aware Byte-Pair Encoding Tokenizer for the Kapampangan
        Language
      </p>

      <div className="two-column">
        <div className="card text-panel">
          <span className="card-pill">Kapampangan</span>
          <textarea
            placeholder="Enter text here"
            maxLength={MAX_LEN}
            value={source}
            onChange={(e) => setSource(e.target.value)}
          />
          <div className="panel-footer">
            <div className="button-row">
              <button className="btn btn-primary" disabled>
                <TranslateIcon className="btn-icon" />
                Translate
              </button>
              <button className="btn btn-secondary" onClick={() => setSource("")}>
                <TrashIcon className="btn-icon" />
                Clear
              </button>
            </div>
            <span className="char-count">
              {source.length}/{MAX_LEN}
            </span>
          </div>
        </div>

        <button className="swap-button" title="Swap languages (UI only)">
          <SwapIcon />
        </button>

        <div className="card text-panel" style={{ position: "relative" }}>
          <span className="card-pill">Filipino</span>
          <textarea placeholder="Translation will show here..." readOnly value="" />
          <button className="copy-button" onClick={handleCopy} title="Copy">
            <CopyIcon />
          </button>
          {copied && (
            <span style={{ position: "absolute", bottom: 18, right: 46, fontSize: 11 }}>
              copied
            </span>
          )}
        </div>
      </div>

      <p className="translator-note">
        Translation is not wired up yet — this page mirrors the design and is ready for the
        NLLB-based translator once it's trained. The working part of this app is the Tokenizer
        tab above.
      </p>
    </div>
  );
}
