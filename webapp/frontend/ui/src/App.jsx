import { useState } from "react";
import Header from "./components/Header.jsx";
import TranslatorPage from "./pages/TranslatorPage.jsx";
import TokenizerPage from "./pages/TokenizerPage.jsx";
import ComparisonPage from "./pages/ComparisonPage.jsx";
import { compareCustom } from "./api.js";

export default function App() {
  const [tab, setTab] = useState("tokenizer");

  // The Comparison tab has no input of its own — it always shows the 3-way
  // comparison for whatever text was last tokenized on the Tokenizer tab.
  // Lifted up here so both tabs share the same source of truth.
  const [comparisonInput, setComparisonInput] = useState("");
  const [comparisonResult, setComparisonResult] = useState(null);
  const [comparisonLoading, setComparisonLoading] = useState(false);
  const [comparisonError, setComparisonError] = useState(null);

  const runComparison = async (text) => {
    setComparisonInput(text);
    setComparisonLoading(true);
    setComparisonError(null);
    try {
      const data = await compareCustom(text);
      setComparisonResult(data);
    } catch (err) {
      setComparisonError(
        err.message.includes("fetch")
          ? "Could not reach the tokenizer backend. Is `python server.py` running on port 8000?"
          : err.message
      );
      setComparisonResult(null);
    } finally {
      setComparisonLoading(false);
    }
  };

  const clearComparison = () => {
    setComparisonInput("");
    setComparisonResult(null);
    setComparisonError(null);
  };

  return (
    <div className="app-shell">
      <Header active={tab} onChange={setTab} />
      {tab === "translator" && <TranslatorPage />}
      {tab === "tokenizer" && (
        <TokenizerPage onTokenized={runComparison} onCleared={clearComparison} />
      )}
      {tab === "comparison" && (
        <ComparisonPage
          input={comparisonInput}
          result={comparisonResult}
          loading={comparisonLoading}
          error={comparisonError}
          onGoToTokenizer={() => setTab("tokenizer")}
        />
      )}
      <div className="footer-bar">
        CANSINO, FAELDONIA, LUCERO, MAGTANONG, MITAL | BSCS 3-5 | All Rights Reserved 2026
      </div>
    </div>
  );
}
