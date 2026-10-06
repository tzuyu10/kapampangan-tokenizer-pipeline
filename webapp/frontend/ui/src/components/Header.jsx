const TABS = [
  { key: "translator-comparison", label: "Translator A/B" },
  { key: "translation-performance", label: "Translation Metrics & Process" },
  { key: "tokenizer", label: "Tokenization" },
  { key: "comparison", label: "Tokenization Comparison & Metrics" },
];

export default function Header({ active, onChange }) {
  return (
    <nav className="top-bar" role="tablist" aria-label="Thesis tool sections">
      {TABS.map((tab) => (
        <button
          key={tab.key}
          id={`tab-${tab.key}`}
          role="tab"
          aria-selected={active === tab.key}
          aria-controls={`panel-${tab.key}`}
          tabIndex={active === tab.key ? 0 : -1}
          className={`tab-button ${active === tab.key ? "active" : ""}`}
          onClick={() => onChange(tab.key)}
          onKeyDown={event => {
            const index = TABS.findIndex(item => item.key === tab.key);
            const next = event.key === "ArrowRight" ? (index + 1) % TABS.length : event.key === "ArrowLeft" ? (index + TABS.length - 1) % TABS.length : event.key === "Home" ? 0 : event.key === "End" ? TABS.length - 1 : null;
            if (next === null) return;
            event.preventDefault(); onChange(TABS[next].key);
            event.currentTarget.parentElement.querySelector(`#tab-${TABS[next].key}`).focus();
          }}
        >
          {tab.label}
        </button>
      ))}
    </nav>
  );
}
