use std::env;
use std::fs;
use std::collections::HashMap;

fn absdiff(a: u32, b:u32) -> u32{
    if a > b {
        a - b
    } else {
        b - a
    }
}

fn score_lists_part1(list1: &mut Vec<u32>, list2: &mut Vec<u32>) -> u32{
    list1.sort();
    list2.sort();

    let mut score: u32 = 0;

    assert_eq!(list1.len(), list2.len());

    while list1.len() != 0{
        score = score + absdiff(
            list1.pop().expect("Not an int"), 
            list2.pop().expect("Not an int"));
    }
    score
}

fn score_lists_part2(list1: &mut Vec<u32>, list2: &mut Vec<u32>) -> u32{

    let mut frequencies:HashMap<u32, u32> = HashMap::new();

    let mut score: u32 = 0;

    for val in list2 {
        let count = frequencies.entry(*val).or_insert(0);
        *count += 1;
    }

    for val in list1 {
        let count = frequencies.get(&val).copied().unwrap_or(0);
        score = score + (*val * count);
    }

    score
}

fn parse_file(input: String) -> (Vec<u32>, Vec<u32>){
    let mut list1: Vec<u32> = Vec::new();
    let mut list2: Vec<u32> = Vec::new();

    for input_line in input.split('\n') {
        let integers: Vec<_> = input_line.
            split_whitespace().
            map(|x| str::parse::<u32>(x).expect("Not an integer")).
            collect();

        if integers.len() == 2 {
            list1.push(integers[0]);
            list2.push(integers[1]);
        } else {
            println!("This line wasn't parsed {input_line}");
        }
    }
    (list1, list2)
}


fn read_file(file_path: &str) -> String{
    let contents: String = fs::read_to_string(file_path)
        .expect("Couldn't parse file");

    contents
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let part: &String = &args[2];

    let input: String = read_file(file_path);

    let (mut list1, mut list2) = parse_file(input);

    if part == "1" {
        let score = score_lists_part1(&mut list1, &mut list2);
        println!("Total score {score}");
    } else if part == "2" {
        let score = score_lists_part2(&mut list1, &mut list2);
        println!("Total score {score}");
    }
}
