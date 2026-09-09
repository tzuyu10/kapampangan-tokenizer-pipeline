const TABS = [
  { key: "translator", label: "Translator" },
  { key: "tokenizer", label: "Tokenizer" },
  { key: "comparison", label: "Comparison" },
];

export default function Header({ active, onChange }) {
  return (
    <div className="top-bar">
      {TABS.map((tab) => (
        <button
          key={tab.key}
          className={`tab-button ${active === tab.key ? "active" : ""}`}
          onClick={() => onChange(tab.key)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
