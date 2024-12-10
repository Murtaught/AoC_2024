use field::Field;

mod pos;
mod field;

fn main() {
    let fld = Field::read_from_file("input").unwrap();
    println!("ans (p1): {}", solve_p1(&fld));
    println!("ans (p2): {}", fld.solve_p2());
}

fn solve_p1(fld: &Field) -> usize {
    fld.find_positions(b'0')
        .map(|pos| fld.compute_score(pos))
        .sum()
}
