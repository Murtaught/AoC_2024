use std::collections::HashMap;

fn main() {
    let input = std::fs::read_to_string("input").unwrap();
    let initial_state: State = input
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();

    let mut cache = Cache::new();
    println!(
        "ans (p1): {}",
        count_recursive(&initial_state, 25, &mut cache)
    );
    println!(
        "ans (p2): {}",
        count_recursive(&initial_state, 75, &mut cache)
    );
}

pub type State = Vec<u64>;

// (x, steps) => numbers count
pub type Cache = HashMap<(u64, usize), usize>;

pub fn count_recursive(state: &State, steps: usize, cache: &mut Cache) -> usize {
    if steps == 0 {
        return state.len();
    }

    state
        .iter()
        .map(|&x| {
            if let Some(&count) = cache.get(&(x, steps)) {
                count
            } else {
                let next_state = simulate_step(&[x]);
                let count = count_recursive(&next_state, steps - 1, cache);
                cache.insert((x, steps), count);
                count
            }
        })
        .sum()
}

pub fn simulate_step(state: &[u64]) -> State {
    let mut next_state = vec![];
    for &x in state {
        if x == 0 {
            next_state.push(1);
        } else if let Some((l, r)) = split_digits(x) {
            next_state.push(l);
            next_state.push(r);
        } else {
            next_state.push(x * 2024);
        }
    }
    next_state
}

pub fn split_digits(x: u64) -> Option<(u64, u64)> {
    let s = format!("{x}");
    let n = s.len();
    if n % 2 == 0 {
        let h = n / 2;
        Some((s[..h].parse().unwrap(), s[h..].parse().unwrap()))
    } else {
        None
    }
}
