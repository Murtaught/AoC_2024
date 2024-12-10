#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Pos {
    pub i: i32,
    pub j: i32,
}

impl Pos {
    pub fn new<T>(i: T, j: T) -> Self
    where
        T: TryInto<i32>,
        T::Error: std::fmt::Debug,
    {
        Self {
            i: i.try_into().unwrap(),
            j: j.try_into().unwrap(),
        }
    }

    pub fn adjust(mut self, di: i32, dj: i32) -> Self {
        self.i += di;
        self.j += dj;
        self
    }
}
