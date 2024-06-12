### NOT WORKING

import operator
import itertools

operations = (operator.add, operator.sub, operator.mul, operator.truediv)
digit_permutations = itertools.permutations(range(10), 4)


def calc_words(current_words, digits):
    # if current_word_list is None:
    #     current_word_list = []
    # if operation_list is None:
    #     operation_list = operations

    # new_words = []

    # if sum(callable(w) for w in current_word) < sum(isinstance(w, int) for w in current_word) - 1:
    #     new_words = [calc_words(current_word + [op], digits, current_word_list, operation_list)
    #                                 for op in operation_list]
    new_words = current_words
    if digits:
        for digit in digits:
            new_digits = digits.copy()
            new_digits.remove(digit)
            new_words = [word + [digit] for word in calc_words(current_words, new_digits)]

    return new_words

    # words = [[]]
    # digits = list(digits_4)
    # for _ in range(7):
    #     new_words = []
    #     add_digit = False
    #     if digits:
    #         digit = digits.pop()
    #         add_digit = True
    #     for word in words:
    #         if add_digit:
    #             new_words.append(word + [digit])
    #         if sum(callable(w) for w in word) < sum(isinstance(w, int) for w in word) - 1:
    #             op_words = [word + [op] for op in operations]
    #             new_words += op_words
    #     words = new_words
    # return words


rpn_words = calc_words([[]], [1,2,3,4])
