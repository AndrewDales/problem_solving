import re
from functools import lru_cache
from pprint import pprint


def parse_bag_string(bag_string):
    # Remove 'bag' or 'bags' and '.'
    bag_string = re.sub(r'(\sbags)|(\sbag)|(\.)', '', bag_string)

    # Find the numbers in the contents
    numbers = [int(num) for num in re.findall(r'[0-9]+', bag_string)]

    # Split at 'contain'
    container, content_names = re.split('contain', bag_string)

    # Strip white space from container
    container = container.strip()

    # Strip digits from the contents
    content_names = re.sub(r'(\d)|(\.)', '', content_names)

    # Split the contents at ',' and strip white space
    if content_names.strip() == 'no other':
        contents = None
    else:
        contents = dict(zip((item.strip() for item in content_names.split(',')),
                            (int(number) for number in numbers)))

    return (container, contents)


@lru_cache(maxsize=1000)
def count_lower_bags(colour_bag):
    if BAG_DATA[colour_bag] is None:
        return 0
    else:
        return sum(bag_number + bag_number * count_lower_bags(bag_colour)
                   for bag_colour, bag_number in BAG_DATA[colour_bag].items())


with open("aoc_2020_7.txt", "r") as file:
    BAG_DATA = dict([parse_bag_string(line) for line in file])

total_bags = count_lower_bags('shiny gold')
print(total_bags)
