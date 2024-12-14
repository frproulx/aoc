use regex::Regex;
use std::env;
use std:: fs;


fn read_file(file_path: &str) -> String{
    let contents: String = fs::read_to_string(file_path)
        .expect("Couldn't parse file");

    contents
}


fn parse_mul(input: String) -> u32 {
    let re = Regex::new(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)").unwrap();
    let caps = re.captures(&input).unwrap();
    str::parse::<u32>(&caps[1]).expect("not an int?") * str::parse::<u32>(&caps[2]).expect("not an int?")
}

fn get_muls(input: String) -> Vec<String> {
    let mul_re = Regex::new(r"mul\([0-9]{1,3},[0-9]{1,3}\)").unwrap();
    let muls: Vec<String> = mul_re.find_iter(&input).map(|m| String::from(m.as_str())).collect();
    muls
}


fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let _part: &String = &args[2];

    let input: String = read_file(file_path);

    let muls = get_muls(input);
    let score: u32 = muls.iter().map(|x| parse_mul(x.clone())).sum();

    println!("Part 1 score: {}", score);

}
