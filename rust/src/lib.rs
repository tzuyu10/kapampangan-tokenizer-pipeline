use pyo3::prelude::*;
use std::collections::{BTreeSet, HashSet};

const PREFIXES: [&str; 15] = [
    "makapag", "mekapag", "maka", "mang", "meka", "meng", "ipa", "mag", "meg",
    "mig", "ka", "ma", "me", "pa", "i",
];
const INFIXES: [&str; 2] = ["in", "um"];
const SUFFIXES: [&str; 1] = ["an"];
const CLITICS: [&str; 9] = ["ku", "la", "mu", "na", "ne", "no", "pa", "ra", "ya"];

#[derive(Clone, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Candidate {
    segments: Vec<String>,
    rule_id: String,
    kind: String,
}

type SegmentOutput = (
    String,
    Vec<String>,
    Vec<usize>,
    Option<String>,
    Option<String>,
    String,
    Vec<String>,
);

fn comparison_key(value: &str) -> String {
    value.to_lowercase()
}

fn char_count(value: &str) -> usize {
    value.chars().count()
}

fn byte_index_at_char(value: &str, position: usize) -> usize {
    value
        .char_indices()
        .nth(position)
        .map_or(value.len(), |(index, _)| index)
}

fn split_at_char(value: &str, position: usize) -> (&str, &str) {
    value.split_at(byte_index_at_char(value, position))
}

fn rule_fragment(value: &str) -> String {
    value.to_uppercase().replace('-', "_")
}

fn mark_boundaries(segments: &[String]) -> Vec<usize> {
    let mut boundaries = Vec::new();
    let mut position = 0;
    for segment in segments.iter().take(segments.len().saturating_sub(1)) {
        position += char_count(segment);
        boundaries.push(position);
    }
    boundaries
}

#[pyclass(name = "Segmenter")]
struct Segmenter {
    roots: HashSet<String>,
    compounds: HashSet<String>,
    variants: HashSet<String>,
}

impl Segmenter {
    fn valid_host(&self, value: &str) -> bool {
        if value.is_empty() {
            return false;
        }
        let key = comparison_key(value);
        self.roots.contains(&key) || self.variants.contains(&key)
    }

    fn try_circumfix(&self, token: &str) -> Vec<Candidate> {
        let lower = comparison_key(token);
        let token_chars = char_count(token);
        let pairs = [
            ("panga", "an", "PANG_PANGA"),
            ("pang", "an", "PANG"),
            ("pam", "an", "PANG_PAM"),
            ("pan", "an", "PANG_PAN"),
            ("ka", "an", "KA"),
            ("pa", "an", "PA"),
        ];
        let mut candidates = Vec::new();
        for (prefix, suffix, rule_name) in pairs {
            let prefix_chars = char_count(prefix);
            let suffix_chars = char_count(suffix);
            if !lower.starts_with(prefix)
                || !lower.ends_with(suffix)
                || token_chars <= prefix_chars + suffix_chars
            {
                continue;
            }
            let (surface_prefix, tail) = split_at_char(token, prefix_chars);
            let core_chars = char_count(tail) - suffix_chars;
            let (core, surface_suffix) = split_at_char(tail, core_chars);
            if self.valid_host(core) {
                candidates.push(Candidate {
                    segments: vec![
                        surface_prefix.to_owned(),
                        core.to_owned(),
                        surface_suffix.to_owned(),
                    ],
                    rule_id: format!("CIRCUMFIX_{rule_name}_AN"),
                    kind: "circumfix".to_owned(),
                });
            }
        }
        candidates
    }

    fn try_prefix(&self, token: &str) -> Vec<Candidate> {
        let lower = comparison_key(token);
        let token_chars = char_count(token);
        let mut candidates = Vec::new();
        for prefix in PREFIXES {
            let prefix_chars = char_count(prefix);
            if !lower.starts_with(prefix) || token_chars <= prefix_chars {
                continue;
            }
            let (surface_prefix, remainder) = split_at_char(token, prefix_chars);
            if self.valid_host(remainder) {
                candidates.push(Candidate {
                    segments: vec![surface_prefix.to_owned(), remainder.to_owned()],
                    rule_id: format!("PREFIX_{}", rule_fragment(prefix)),
                    kind: "prefix".to_owned(),
                });
            }
        }
        candidates
    }

    fn try_infix(&self, token: &str) -> Vec<Candidate> {
        let token_chars = char_count(token);
        let mut candidates = Vec::new();
        for infix in INFIXES {
            let infix_chars = char_count(infix);
            if token_chars <= 1 + infix_chars {
                continue;
            }
            let (left, tail) = split_at_char(token, 1);
            let (surface_infix, right) = split_at_char(tail, infix_chars);
            if comparison_key(surface_infix) != infix {
                continue;
            }
            let reconstructed = format!("{left}{right}");
            if self.valid_host(&reconstructed) {
                candidates.push(Candidate {
                    segments: vec![
                        left.to_owned(),
                        surface_infix.to_owned(),
                        right.to_owned(),
                    ],
                    rule_id: format!("INFIX_{}", rule_fragment(infix)),
                    kind: "infix".to_owned(),
                });
            }
        }
        candidates
    }

    fn try_suffix(&self, token: &str) -> Vec<Candidate> {
        let lower = comparison_key(token);
        let token_chars = char_count(token);
        let mut candidates = Vec::new();
        for suffix in SUFFIXES {
            let suffix_chars = char_count(suffix);
            if !lower.ends_with(suffix) || token_chars <= suffix_chars {
                continue;
            }
            let (remainder, surface_suffix) = split_at_char(token, token_chars - suffix_chars);
            if self.valid_host(remainder) {
                candidates.push(Candidate {
                    segments: vec![remainder.to_owned(), surface_suffix.to_owned()],
                    rule_id: format!("SUFFIX_{}", rule_fragment(suffix)),
                    kind: "suffix".to_owned(),
                });
            }
        }
        candidates
    }

    fn try_clitic(&self, token: &str) -> Vec<Candidate> {
        let lower = comparison_key(token);
        let token_chars = char_count(token);
        let mut candidates = Vec::new();
        for clitic in CLITICS {
            let clitic_chars = char_count(clitic);
            if !lower.ends_with(clitic) || token_chars <= clitic_chars {
                continue;
            }
            let (host, surface_clitic) = split_at_char(token, token_chars - clitic_chars);
            let host_key = comparison_key(host);
            if self.roots.contains(&host_key)
                || self.variants.contains(&host_key)
                || self.compounds.contains(&host_key)
            {
                candidates.push(Candidate {
                    segments: vec![host.to_owned(), surface_clitic.to_owned()],
                    rule_id: format!("CLITIC_{}", rule_fragment(clitic)),
                    kind: "clitic".to_owned(),
                });
            }
        }
        candidates
    }

    fn resolve(&self, token: &str, stage: &str, candidates: Vec<Candidate>) -> Option<SegmentOutput> {
        if candidates.is_empty() {
            return None;
        }
        let distinct: BTreeSet<Candidate> = candidates.into_iter().collect();
        if distinct.len() > 1 {
            let rule_ids = distinct
                .iter()
                .map(|candidate| candidate.rule_id.as_str())
                .collect::<Vec<_>>()
                .join("|");
            return Some((
                token.to_owned(),
                vec![token.to_owned()],
                Vec::new(),
                None,
                Some(stage.to_owned()),
                "ambiguous".to_owned(),
                vec![
                    "normalize:nfc".to_owned(),
                    format!("stage:{stage}"),
                    format!("ambiguous:{rule_ids}"),
                ],
            ));
        }
        let candidate = distinct.into_iter().next().expect("one candidate");
        let boundaries = mark_boundaries(&candidate.segments);
        Some((
            token.to_owned(),
            candidate.segments,
            boundaries,
            Some(candidate.rule_id.clone()),
            Some(candidate.kind),
            "accepted".to_owned(),
            vec![
                "normalize:nfc".to_owned(),
                format!("stage:{stage}"),
                format!("accept:{}", candidate.rule_id),
            ],
        ))
    }

    fn segment_internal(&self, token: &str) -> SegmentOutput {
        if token.is_empty() {
            return (
                String::new(),
                Vec::new(),
                Vec::new(),
                None,
                None,
                "empty".to_owned(),
                vec!["normalize:nfc".to_owned(), "empty".to_owned()],
            );
        }
        let key = comparison_key(token);
        if self.compounds.contains(&key) {
            return (
                token.to_owned(),
                vec![token.to_owned()],
                Vec::new(),
                Some("PROTECT_COMPOUND".to_owned()),
                Some("compound".to_owned()),
                "protected_compound".to_owned(),
                vec!["normalize:nfc".to_owned(), "protect:compound".to_owned()],
            );
        }
        if self.roots.contains(&key) || self.variants.contains(&key) {
            return (
                token.to_owned(),
                vec![token.to_owned()],
                Vec::new(),
                Some("PROTECT_ROOT".to_owned()),
                Some("root".to_owned()),
                "protected_root".to_owned(),
                vec!["normalize:nfc".to_owned(), "protect:root".to_owned()],
            );
        }
        if let Some(result) = self.resolve(token, "circumfix", self.try_circumfix(token)) {
            return result;
        }
        if let Some(result) = self.resolve(token, "prefix", self.try_prefix(token)) {
            return result;
        }
        if let Some(result) = self.resolve(token, "infix", self.try_infix(token)) {
            return result;
        }
        if let Some(result) = self.resolve(token, "suffix", self.try_suffix(token)) {
            return result;
        }
        if let Some(result) = self.resolve(token, "clitic", self.try_clitic(token)) {
            return result;
        }
        (
            token.to_owned(),
            vec![token.to_owned()],
            Vec::new(),
            None,
            None,
            "unchanged".to_owned(),
            vec![
                "normalize:nfc".to_owned(),
                "unchanged:no_valid_analysis".to_owned(),
            ],
        )
    }
}

#[pymethods]
impl Segmenter {
    #[new]
    fn new(roots: Vec<String>, compounds: Vec<String>, variants: Vec<String>) -> Self {
        Self {
            roots: roots.into_iter().map(|value| comparison_key(&value)).collect(),
            compounds: compounds
                .into_iter()
                .map(|value| comparison_key(&value))
                .collect(),
            variants: variants
                .into_iter()
                .map(|value| comparison_key(&value))
                .collect(),
        }
    }

    fn segment(&self, token: &str) -> SegmentOutput {
        self.segment_internal(token)
    }

    fn segment_batch(&self, tokens: Vec<String>) -> Vec<SegmentOutput> {
        tokens
            .iter()
            .map(|token| self.segment_internal(token))
            .collect()
    }
}

#[pymodule]
fn _rust_segmenter(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_class::<Segmenter>()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::Segmenter;

    fn segmenter() -> Segmenter {
        Segmenter::new(
            vec!["kan".to_owned(), "sulat".to_owned()],
            vec!["bahay-basa".to_owned()],
            Vec::new(),
        )
    }

    #[test]
    fn infix_reconstructs_root() {
        let output = segmenter().segment_internal("kuman");
        assert_eq!(output.1, vec!["k", "um", "an"]);
        assert_eq!(output.3.as_deref(), Some("INFIX_UM"));
    }

    #[test]
    fn invalid_host_is_unchanged() {
        let output = segmenter().segment_internal("maxyz");
        assert_eq!(output.1, vec!["maxyz"]);
        assert_eq!(output.5, "unchanged");
    }
}
