use std::env;
use std::fs;

struct Report {
    levels: Vec<i16>,
}

impl Report {
    fn assess_safety(&mut self) -> bool{

        let steps: Vec<i16> = self.levels.windows(2).map(|x| &x[1] - &x[0]).collect();

        let all_positive: bool = steps.iter().all(|&x| x > 0);
        let all_negative: bool = steps.iter().all(|&x| x < 0);


        let correct_range: bool = steps.iter().all(|&x| (x.abs() >= 1) && (x.abs() <= 3));

        (all_positive || all_negative) && correct_range

    }
}

impl Report {
    fn assess_safety_part2(&mut self) -> bool{

        let steps: Vec<i16> = self.levels.windows(2).map(|x| &x[1] - &x[0]).collect();

        let all_positive: Vec<bool> = steps.iter().map(|&x| x > 0).collect();
        let all_negative: Vec<bool> = steps.iter().map(|&x| x < 0).collect();

        let correct_range: Vec<bool> = steps.iter().map(|&x| (x.abs() >= 1) && (x.abs() <= 3)).collect();

        let level_safety: Vec<bool> = all_positive.
            iter().
            zip(all_negative.iter()).
            map(|(x, y)| *x || *y).
            zip(correct_range.iter()).
            map(|(x, y)| x && *y).
            collect();

        for l in &level_safety {println!("{}", l);}
        println!("\n");

        level_safety.iter().filter(|x| !*x).count() <= 1

    }
}


fn read_file(file_path: &str) -> String{
    let contents: String = fs::read_to_string(file_path)
        .expect("Couldn't parse file");

    contents
}

fn parse_file(input: String) -> Vec<Report> {
    let mut reports = Vec::<Report>::new();

    for input_line in input.split('\n'){
        let levels: Vec<i16> = input_line.
            split_whitespace().
            map(|x| str::parse::<i16>(x).expect("Not an integer")).
            collect();

        if levels.len() <= 1 {
            continue;
        }
        let report = Report{levels};
        reports.push(report);
    }
    reports
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let part: &String = &args[2];

    let input: String = read_file(file_path);

    let mut reports = parse_file(input);

    if part == "1" {
        let safety_eval = reports.iter_mut().map(|x| x.assess_safety());

        let score: usize = safety_eval.filter(|x| *x).count();

        println!("Part 1 score {score}");
    } else if part == "2" {
        let safety_eval = reports.iter_mut().map(|x| x.assess_safety_part2());
        let score: usize = safety_eval.filter(|x| *x).count();
        println!("Part 2 score {score}");
    }
}
