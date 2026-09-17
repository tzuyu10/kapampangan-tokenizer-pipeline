// Small hand-written inline icons (stroke = currentColor) so the app has
// zero icon-library dependency.

export function TranslateIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" {...props}>
      <path d="M4 6h9" strokeLinecap="round" />
      <path d="M8.5 4v2.2c0 3.2-2 5.8-4.5 5.8" strokeLinecap="round" />
      <path d="M5 7.5c0 1.8 2.2 3.3 5 3.3" strokeLinecap="round" />
      <path d="M13 21l4-9 4 9" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M14.5 18h5" strokeLinecap="round" />
    </svg>
  );
}

export function TrashIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" {...props}>
      <path d="M4 7h16" strokeLinecap="round" />
      <path d="M9 7V4h6v3" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M6 7l1 13h10l1-13" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M10 11v6M14 11v6" strokeLinecap="round" />
    </svg>
  );
}

export function ArrowRightIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" {...props}>
      <path d="M4 12h16" strokeLinecap="round" />
      <path d="M13 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function SwapIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" {...props}>
      <path d="M4 8h13" strokeLinecap="round" />
      <path d="M14 4l3 4-3 4" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M20 16H7" strokeLinecap="round" />
      <path d="M10 12l-3 4 3 4" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function CopyIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" {...props}>
      <rect x="9" y="9" width="11" height="11" rx="2" />
      <path d="M5 15V5a2 2 0 0 1 2-2h10" />
    </svg>
  );
}

export function CompareIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" {...props}>
      <path d="M4 7h13" strokeLinecap="round" />
      <path d="m14 4 3 3-3 3" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M20 17H7" strokeLinecap="round" />
      <path d="m10 14-3 3 3 3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
