pub fn score_runtime_spike(latency_ms: f64, baseline_ms: f64) -> f64 {
    if baseline_ms <= 0.0 {
        return 0.0;
    }
    let ratio = latency_ms / baseline_ms;
    ((ratio - 1.0).max(0.0) * 25.0).min(100.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn score_increases_for_spike() {
        assert!(score_runtime_spike(320.0, 100.0) > 0.0);
    }
}

