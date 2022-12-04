import re
from functools import lru_cache
from pprint import pprint


def parse_bag_string(bag_string):
    # Remove 'bag' or 'bags' and '.'
    bag_string = re.sub(r'(\sbags)|(\sbag)|(\d)', '', bag_string)

    # Split at 'contain'
    container, contents = re.split('contain', bag_string)

    # Strip white space from container
    container = container.strip()

    # Strip numbers and '.' from the contents
    contents = re.sub(r'(\d)|(\.)', '', contents)

    # Split the contents at ',' and strip white space
    if contents.strip() == 'no other':
        contents = None
    else:
        contents = tuple(item.strip() for item in contents.split(','))

    return (container, contents)


@lru_cache(maxsize=1000)
def contains_bag_colour(colour_bag, colour='shiny gold'):
    if BAG_DATA[colour_bag] is None:
        return False
    elif colour in BAG_DATA[colour_bag]:
        return True
    else:
        return any(contains_bag_colour(bag_colour)
                   for bag_colour in BAG_DATA[colour_bag])


with open("aoc_2020_7.txt", "r") as file:
    BAG_DATA = dict([parse_bag_string(line) for line in file])

valid_bag_colours = [bag_colour
                     for bag_colour in BAG_DATA.keys()
                     if contains_bag_colour(bag_colour)]

print(len(valid_bag_colours))
