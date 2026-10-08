import { useCallback, useRef, useState } from "react";
import Header from "./components/Header.jsx";
import TranslationPerformancePage from "./pages/TranslationPerformancePage.jsx";
import TranslatorComparisonPage from "./pages/TranslatorComparisonPage.jsx";
import TokenizerPage from "./pages/TokenizerPage.jsx";
import ComparisonPage from "./pages/ComparisonPage.jsx";
import { compareCustom } from "./api.js";

export default function App() {
  const [tab, setTab] = useState("translator-comparison");
  const [source, setSource] = useState("");
  const [translationResult, setTranslationResult] = useState(null);
  const [translationLoading, setTranslationLoading] = useState(false);
  const [translationError, setTranslationError] = useState(null);

  // The Comparison tab has no input of its own — it always shows the 3-way
  // comparison for whatever text was last tokenized on the Tokenizer tab.
  // Lifted up here so both tabs share the same source of truth.
  const [comparisonInput, setComparisonInput] = useState("");
  const [comparisonResult, setComparisonResult] = useState(null);
  const [comparisonLoading, setComparisonLoading] = useState(false);
  const [comparisonError, setComparisonError] = useState(null);
  const comparisonRequest = useRef(0);

  const runComparison = async (text) => {
    const request = ++comparisonRequest.current;
    setComparisonInput(text);
    setComparisonLoading(true);
    setComparisonError(null);
    try {
      const data = await compareCustom(text);
      if (request !== comparisonRequest.current) return;
      setComparisonResult(data);
    } catch (err) {
      if (request !== comparisonRequest.current) return;
      setComparisonError(
        err.message.includes("fetch")
          ? "Could not reach the tokenizer backend. Is `python server.py` running on port 8000?"
          : err.message
      );
      setComparisonResult(null);
    } finally {
      if (request === comparisonRequest.current) setComparisonLoading(false);
    }
  };

  const clearComparison = useCallback(() => {
    comparisonRequest.current += 1;
    setComparisonInput("");
    setComparisonResult(null);
    setComparisonLoading(false);
    setComparisonError(null);
  }, []);

  return (
    <div className="app-shell">
      <Header active={tab} onChange={setTab} />
      <section className="tab-panel" role="tabpanel" id="panel-translator-comparison" aria-labelledby="tab-translator-comparison" hidden={tab !== "translator-comparison"}>
        <TranslatorComparisonPage source={source} setSource={setSource} result={translationResult} setResult={setTranslationResult}
          loading={translationLoading} setLoading={setTranslationLoading} error={translationError} setError={setTranslationError}
          onViewPerformance={() => setTab("translation-performance")} />
      </section>
      <section className="tab-panel" role="tabpanel" id="panel-translation-performance" aria-labelledby="tab-translation-performance" hidden={tab !== "translation-performance"}>
        <TranslationPerformancePage source={source} result={translationResult} loading={translationLoading} error={translationError}
          onGoToTranslator={() => setTab("translator-comparison")} />
      </section>
      <section className="tab-panel" role="tabpanel" id="panel-tokenizer" aria-labelledby="tab-tokenizer" hidden={tab !== "tokenizer"}>
        <TokenizerPage translationSource={source} onTokenized={runComparison} onCleared={clearComparison} />
      </section>
      <section className="tab-panel" role="tabpanel" id="panel-comparison" aria-labelledby="tab-comparison" hidden={tab !== "comparison"}>
        <ComparisonPage
          input={comparisonInput}
          result={comparisonResult}
          loading={comparisonLoading}
          error={comparisonError}
          onGoToTokenizer={() => setTab("tokenizer")}
        />
      </section>
      <div className="footer-bar">
        CANSINO, FAELDONIA, LUCERO, MAGTANONG, MITAL | BSCS 3-5 | All Rights Reserved 2026
      </div>
    </div>
  );
}
