import re


def valid_passport(passport):
    def valid_height(hgt_str):
        unit = hgt_str[-2:]
        valid = (((unit == "cm") and (150 <= int(hgt_str[:-2]) <= 193)) or
                 ((unit == "in") and (59 <= int(hgt_str[:-2]) <= 76)))
        return valid

    rqd_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    eye_colours = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    hex_regex = "^#[A-Fa-f0-9]{6}$"

    if not rqd_fields.issubset(passport.keys()):
        valid = False
    else:
        valid = ((1920 <= int(passport['byr']) <= 2002) and
                 (2010 <= int(passport["iyr"]) <= 2020) and
                 (2020 <= int(passport["eyr"]) <= 2030) and
                 (valid_height(passport["hgt"])) and
                 (bool(re.match(hex_regex, passport["hcl"])) and
                  (passport['ecl'] in eye_colours) and
                  (passport['pid'].isdigit()) and
                  (len(passport['pid']) == 9)))

    return valid


with open("aoc_2020_4.txt", "r") as file:
    raw_data = [line.strip() if len(line) > 1 else "!" for line in file]

data_string = " ".join(raw_data)
parsed_data = data_string.split("!")

passport_data = [dict([item.split(":") for item in line.strip().split(" ")]) for line in parsed_data]

sum_valid = sum(valid_passport(passport) for passport in passport_data)
print(sum_valid)
