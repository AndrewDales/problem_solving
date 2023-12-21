import re
import operator as op
from collections import namedtuple
from dataclasses import dataclass
from typing import Callable
import copy

with open("data/aoc_input_2023_19.txt") as file:
    file_contents = file.read()
    file_workflows, file_ratings = file_contents.split('\n\n')


@dataclass
class Rule:
    category: str = ''
    op: Callable[[int, int], bool] | None = None
    threshold: int = 0
    destination: str = ''


class RatingRange:
    x: tuple[int, int] = (1, 4001)
    m: tuple[int, int] = (1, 4001)
    a: tuple[int, int] = (1, 4001)
    s: tuple[int, int] = (1, 4001)

    def number_possibilities(self):
        return ((self.x[1] - self.x[0]) *
                (self.m[1] - self.m[0]) *
                (self.a[1] - self.a[0]) *
                (self.s[1] - self.s[0]))


def parse_rule(rule_string):
    colon_loc = rule_string.find(':')
    if colon_loc == -1:
        rule = Rule(destination=rule_string)
    else:
        rule_parts = re.match(r'([a-z])([<>])(\d+):(\w+)', rule_string).groups()
        if rule_parts[1] == '<':
            rule_op = op.lt
        else:
            rule_op = op.gt
        rule = Rule(category=rule_parts[0],
                    op=rule_op,
                    threshold=int(rule_parts[2]),
                    destination=rule_parts[3],
                    )
    return rule


def parse_workflow_statement(workflow_statement):
    workflow_label, rules_statement = re.match(r'([a-z]+){(.*)}', workflow_statement).groups()
    rule_strings = rules_statement.split(',')
    rules = [parse_rule(rule) for rule in rule_strings]
    return workflow_label, rules


def test_part(part, workflow_label='in'):
    rules = workflows[workflow_label]
    # print(workflow_label)
    test_output = False
    for rule in rules:
        if not rule.category:
            result = rule.destination
        elif rule.op(getattr(part, rule.category), rule.threshold):
            result = rule.destination
        else:
            continue
        if result == 'A':
            test_output = True
            break
        elif result == 'R':
            test_output = False
            break
        else:
            test_output = test_part(part, result)
            break

    return test_output


def test_part_ranges(current_ranges, workflow_label='in'):
    num_combos = 0
    rules = workflows[workflow_label]

    for rule in rules:
        result = rule.destination
        accepted_ranges = copy.copy(current_ranges)

        if rule.category:
            category_range = getattr(current_ranges, rule.category)

            if category_range[0] < rule.threshold < category_range[1]:
                result = rule.destination

                if rule.op == op.gt:
                    # don't meet criteria - part to go through to the next rule
                    setattr(current_ranges, rule.category, (category_range[0], rule.threshold+1))
                    # do meet criteria to be sent to the new destination
                    setattr(accepted_ranges, rule.category, (rule.threshold+1, category_range[1]))
                if rule.op == op.lt:
                    setattr(current_ranges, rule.category, (rule.threshold, category_range[1]))
                    setattr(accepted_ranges, rule.category, (category_range[0], rule.threshold))
            # Rule does not apply to the range of values in current_ranges - continue to the next rule
            else:
                continue

        if result == 'A':
            num_combos += accepted_ranges.number_possibilities()
        elif result == 'R':
            pass
        else:
            num_combos += test_part_ranges(accepted_ranges, result)

    return num_combos



PartRating = namedtuple('PartRating', "x m a s")
# RatingRange = namedtuple('RatingRange', "x m a s", defaults=[(1, 4001)]*4)

ratings = re.findall(r'{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}', file_ratings)
part_ratings = [PartRating(*(int(v) for v in rating)) for rating in ratings]
workflows = dict(parse_workflow_statement(stmt) for stmt in file_workflows.split('\n'))

print(f'Solution to Day 19, part 1 is {sum(sum(rating) for rating in part_ratings if test_part(rating))}')

initial_ranges = RatingRange()

accepted_range_number = test_part_ranges(initial_ranges, 'in')
print(f'Solution to Day 19, part 2 is {accepted_range_number}')
