export default function ExampleChips({ examples, onPick }) {
  if (!examples) return null;

  const chips = [
    ...examples.words.slice(0, 4).map((w) => ({ label: w.text, value: w.text })),
    ...examples.sentences.slice(0, 2).map((s, i) => ({
      label: `sentence ${i + 1} (with gold |)`,
      value: s.text,
    })),
  ];

  return (
    <div>
      <div className="example-row">
        {chips.map((c, i) => (
          <button key={i} className="example-chip" onClick={() => onPick(c.value)}>
            {c.label}
          </button>
        ))}
      </div>
      <p className="example-hint">
        Tip: mark gold morpheme boundaries with <code>|</code> (e.g. <code>s|in|ulat</code>) to
        also compute Boundary F1 and Consistency F1 — otherwise only Fertility is shown.
      </p>
    </div>
  );
}
