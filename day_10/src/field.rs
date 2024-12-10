use std::{collections::{HashMap, HashSet, VecDeque}, io, path::Path};

use crate::pos::Pos;

#[derive(Debug, Clone)]
pub struct Field {
    fld: Vec<Vec<u8>>,
}

impl Field {
    pub fn read_from_file(path: impl AsRef<Path>) -> io::Result<Self> {
        let content = std::fs::read_to_string(path)?;
        Ok(Self {
            fld: content
                .lines()
                .map(|line| line.trim().bytes().map(|c| c - b'0').collect())
                .collect(),
        })
    }

    pub fn height(&self) -> i32 {
        self.fld.len() as i32
    }

    pub fn width(&self) -> i32 {
        self.fld[0].len() as i32
    }

    pub fn get(&self, pos: Pos) -> u8 {
        if pos.i < 0 || pos.i >= self.height() || pos.j < 0 || pos.j >= self.width() {
            return u8::MAX;
        }

        self.fld[pos.i as usize][pos.j as usize]
    }

    pub fn find_positions(&self, c: u8) -> impl Iterator<Item = Pos> {
        let mut ret = vec![];
        for i in 0..self.height() {
            for j in 0..self.width() {
                let pos = Pos::new(i, j);
                if self.get(pos) == (c - b'0') {
                    ret.push(pos);
                }
            }
        }
        ret.into_iter()
    }

    // Score is the count of peaks (`== 9_u8`) reachable from `pos`.
    pub fn compute_score(&self, pos: Pos) -> usize {
        let mut peaks = HashSet::<Pos>::new();

        let mut queue = VecDeque::<Pos>::new();
        queue.push_back(pos);

        let try_neighbor = |p: Pos, h: u8, q: &mut VecDeque<Pos>| {
            if self.get(p) == h + 1 {
                q.push_back(p);
            }
        };

        while let Some(cur) = queue.pop_front() {
            let height = self.get(cur);
            if height == 9 {
                peaks.insert(cur);
            }

            try_neighbor(cur.adjust(-1,  0), height, &mut queue);
            try_neighbor(cur.adjust( 0,  1), height, &mut queue);
            try_neighbor(cur.adjust( 1,  0), height, &mut queue);
            try_neighbor(cur.adjust( 0, -1), height, &mut queue);
        }

        peaks.len()
    }

    pub fn solve_p2(&self) -> usize {
        let mut scores: HashMap<Pos, usize> = self
            .find_positions(b'9')
            .map(|pos| (pos, 1))
            .collect();

        let mut queue: VecDeque<Pos> = self
            .find_positions(b'9')
            .collect();

        let mut total_score = 0_usize;

        while let Some(cur) = queue.pop_front() {
            let height = self.get(cur);
            let score = *scores.get(&cur).unwrap();

            if height == 0 {
                total_score += score;
                continue;
            }

            for (di, dj) in [(-1, 0), (0, 1), (1, 0), (0, -1)] {
                let nbr = cur.adjust(di, dj);
                if self.get(nbr).saturating_add(1) == height {
                    if let Some(nbr_score) = scores.get(&nbr).copied() {
                        scores.insert(nbr, nbr_score + score);
                    } else {
                        scores.insert(nbr, score);
                        queue.push_back(nbr);
                    }
                }
            }
        }

        total_score
    }
}
