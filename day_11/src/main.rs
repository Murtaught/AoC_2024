fn main() {
    let input = std::fs::read_to_string("input").unwrap();
    let initial_state: State = input
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();

    println!("ans (p1): {}", simulate(initial_state, 25).len());
}

pub type State = Vec<u64>;

pub fn simulate(mut state: State, steps: usize) -> State {
    eprintln!("Initial state: {state:?}");
    for _step_no in 0..steps {
        state = simulate_step(&state);
        // eprintln!("After step #{}: {state:?}", _step_no + 1);
    }
    state
}

pub fn simulate_step(state: &State) -> State {
    let mut next_state = vec![];
    for &x in state {
        if x == 0 {
            next_state.push(1);
        }
        else if let Some((l, r)) = split_digits(x) {
            next_state.push(l);
            next_state.push(r);
        }
        else {
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
