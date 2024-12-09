use std::{cmp::min, collections::HashSet};

#[derive(Debug, Clone)]
pub enum Span {
    File { id: usize, len: usize },
    FreeSpace { len: usize },
}

impl Span {
    pub fn is_file(&self) -> bool {
        matches!(self, Span::File { .. })
    }

    pub fn is_free_space(&self) -> bool {
        matches!(self, Span::FreeSpace { .. })
    }

    pub fn file_id(&self) -> Option<usize> {
        match self {
            Span::File { id, .. } => Some(*id),
            _ => None,
        }
    }

    pub fn len(&self) -> usize {
        match self {
            Span::File { len, .. } => *len,
            Span::FreeSpace { len } => *len,
        }
    }
}

pub fn parse_dense_format(s: &[u8]) -> Vec<Span> {
    let mut file = true;
    let mut file_id = 0;
    let mut ret = vec![];
    for &c in s {
        let len = (c - b'0') as usize;
        if file {
            ret.push(Span::File { id: file_id, len });
            file_id += 1;
        } else {
            ret.push(Span::FreeSpace { len });
        }
        file = !file;
    }
    ret
}

pub fn debug_print(spans: &[Span]) {
    for span in spans {
        let c = if let Span::File { id, .. } = span {
            (b'0' + *id as u8) as char
        }
        else {
            '.'
        };

        for _ in 0..span.len() {
            eprint!("{c}");
        }
    }
    eprintln!();
}

pub fn compact_blocks(spans: &[Span]) -> Vec<Span> {
    if spans.is_empty() {
        return vec![];
    }

    let mut ret = vec![];
    let mut l = 0;
    let mut r = spans.len() - 1;

    let mut cur_file_id = 0_usize;
    let mut remaining_file_len = 0_usize;
    let mut remaining_fs_len = 0_usize;

    while l < r || (remaining_fs_len > 0 && remaining_file_len > 0) {
        if remaining_fs_len > 0 {
            if remaining_file_len > 0 {
                let new_len = min(remaining_file_len, remaining_fs_len);
                remaining_file_len -= new_len;
                remaining_fs_len -= new_len;
                ret.push(Span::File {
                    id: cur_file_id,
                    len: new_len,
                });
            } else {
                if let Span::File {
                    id: file_id,
                    len: file_len,
                } = spans[r]
                {
                    cur_file_id = file_id;
                    remaining_file_len = file_len;
                }

                r -= 1;
            }
        } else {
            if let Span::FreeSpace { len: fs_len } = spans[l] {
                remaining_fs_len = fs_len;
            } else {
                ret.push(spans[l].clone());
            }

            l = min(l + 1, spans.len() - 1);
        }
    }

    if remaining_file_len > 0 {
        ret.push(Span::File {
            id: cur_file_id,
            len: remaining_file_len,
        });
    }

    ret
}

pub fn compact_files(spans: &[Span]) -> Vec<Span> {
    // debug_print(&spans);

    let mut ret = vec![];
    let mut moved_ids = HashSet::<usize>::new();

    for span in spans {
        // debug_print(&ret);

        if span.is_free_space() || moved_ids.contains(&span.file_id().unwrap()) {
            let mut remaining_fs_len = span.len();
            while remaining_fs_len > 0 {
                // Let's try to fill it.
                let file = spans
                    .iter()
                    .rev()
                    .filter(|sp| sp.is_file())
                    .filter(|file| !moved_ids.contains(&file.file_id().unwrap()))
                    .filter(|file| file.len() <= remaining_fs_len)
                    .next();

                if let Some(Span::File {
                    id: file_id,
                    len: file_len,
                }) = file
                {
                    moved_ids.insert(*file_id);
                    ret.push(file.unwrap().clone());
                    remaining_fs_len -= file_len;
                }
                else {
                    ret.push(Span::FreeSpace { len: remaining_fs_len });
                    remaining_fs_len = 0;
                }
            }
        }
        else {
            assert!(span.is_file());
            assert!(!moved_ids.contains(&span.file_id().unwrap()));
            ret.push(span.clone());
            moved_ids.insert(span.file_id().unwrap());
        }
    }
    ret
}

pub fn compute_hash(spans: &[Span]) -> usize {
    let mut ret = 0_usize;
    let mut i = 0_usize;
    for span in spans {
        if span.is_free_space() {
            i += span.len();
            continue;
        }

        for _ in 0..span.len() {
            ret += i * span.file_id().unwrap();
            i += 1;
        }
    }
    ret
}

fn main() {
    let input = std::fs::read_to_string("input").unwrap();
    let input = input.trim_end().as_bytes();
    let spans = parse_dense_format(input);
    println!("ans (p1): {}", compute_hash(&compact_blocks(&spans)));
    println!("ans (p2): {}", compute_hash(&compact_files(&spans)));
}
