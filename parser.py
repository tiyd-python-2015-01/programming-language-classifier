import re
import numpy as np


"""The Parser module will provide methods for parsing information from a
string representing a source code document, as well as a method for reading
the file"""


def read_file(file_path):
    with open(file_path) as source_file:
        source_text = source_file.read()
    return source_text


def split_into_lines(source_text):
    return source_text.splitlines()


def identify_comment_type(source_lines):
    comment_types = [r"\w*/\*+", r"\w*\(\*+", r"\w*;;+", r"\w*//+",
                     r"\w*--+", r"\w*\#+"]

    for line in source_lines:
        for index, c_type in enumerate(comment_types):
            if re.search(r"{} ?(\w+ )+".format(c_type), line):
                return index
    return -1


def identify_comment_blocks(c_type, source_lines):
    block_start = [r"\w*/\*+", r"\w*\(\*+"]
    block_stop = [r"\*+/", r"\*+\)"]
    in_block = False
    to_remove = []

    for line in source_lines:
        if in_block == True and re.search(block_stop[c_type], line):
            to_remove.append(line)
            in_block = False
        elif in_block == True:
            to_remove.append(line)
        elif re.match(block_start[c_type], line):
            to_remove.append(line)
            in_block = True
    return to_remove


def strip_comments(c_type, source_lines):
    comment_types = [r"/\*+", r"\(\*+", r";;+", r"//+", r"--+", r"\#+"]
    items_to_remove = []

    if c_type == 0 or c_type == 1:
        items_to_remove.extend(identify_comment_blocks(c_type, source_lines))
    if c_type == 0:
        c_type = 3
    if c_type >= 3:
        for line in source_lines:
            if re.match(comment_types[c_type], line):
                items_to_remove.append(line)

    stripped_source_lines = remove_items(items_to_remove, source_lines)
    if c_type >= 3:
        stripped_source_lines = strip_inline_comments(c_type,
                                                      stripped_source_lines)
    return stripped_source_lines


def remove_items(items, source_lines):
    for item in items:
        try:
            source_lines.remove(item)
        except ValueError:
            continue
    return source_lines


def strip_inline_comments(c_type, source_lines):
    comment_types = [r"/\*+", r"\(\*+", r";;+", r"//+", r"--+", r"\#+"]
    stripped_lines = []
    for line in source_lines:
        if re.search(comment_types[c_type], line):
            index = re.search(comment_types[c_type], line).span()[0]
            stripped_lines.append(line[:index])
        else:
            stripped_lines.append(line)
    return stripped_lines


def count_characters(source_lines):
    source_text = "\n".join(source_lines)
    return len(source_text)


def identify_print_style(source_lines):
    for line in source_lines:
        if line.find("puts") > -1:
            return 0
        elif line.find("println") > -1:
            return 1
        elif line.find("printf") > -1:
            return 2
        elif line.find("print") > -1:
            return 3
    return -1


def count_parentheses(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count("(") + source_text.count(")")
    return total_count / length_of_source


def count_braces(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count("{") + source_text.count("}")
    return total_count / length_of_source


def count_double_colons(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count("::")
    return total_count / length_of_source


def count_semi_colons(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count(";")
    return total_count / length_of_source


def count_dollar_signs(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count("$")
    return total_count / length_of_source


def count_question_marks(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count("?")
    return total_count / length_of_source


def count_pipes(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count("|")
    return total_count / length_of_source


def count_percent_signs(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count("%")
    return total_count / length_of_source


def count_at_symbols(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count("@")
    return total_count / length_of_source


def count_double_period(source_list, length_of_source):
    source_text = "\n".join(source_list)
    total_count = source_text.count("..")
    return total_count / length_of_source


def check_double_plus_minus(source_list):
    source_text = "\n".join(source_list)
    if source_text.find("++") > -1 or source_text.find("--") > -1:
        return 1
    else:
        return 0


def check_colon_equals(source_list):
    source_text = "\n".join(source_list)
    if source_text.find(":=") > -1:
        return 1
    else:
        return 0


def check_dash_arrow(source_list):
    source_text = "\n".join(source_list)
    if source_text.find("->") > -1:
        return 1
    else:
        return 0


def check_reverse_dash_arrow(source_list):
    source_text = "\n".join(source_list)
    if source_text.find("<-") > -1:
        return 1
    else:
        return 0

def check_equals_arrow(source_list):
    source_text = "\n".join(source_list)
    if source_text.find("=>") > -1:
        return 1
    else:
        return 0


def check_for_function(source_list):
    source_text = "\n".join(source_list)
    if source_text.find("function") > -1:
        return 1
    else:
        return 0


def check_for_public(source_list):
    source_text = "\n".join(source_list)
    if source_text.find("public") > -1:
        return 1
    else:
        return 0

        
def parse_and_score(file_location):
    scores = []
    source_text = read_file(file_location)
    source_length = count_characters(source_text)
    listed_source_text = split_into_lines(source_text)
    comment_style = identify_comment_type(listed_source_text)
    listed_source_text = strip_comments(comment_style, listed_source_text)
    print_style = identify_print_style(listed_source_text)

    parentheses_proportion = count_parentheses(listed_source_text,
                                               source_length)
    curly_brace_proportion = count_braces(listed_source_text, source_length)
    double_colon_proportion = count_double_colons(listed_source_text,
                                                  source_length)
    semi_colon_proportion = count_semi_colons(listed_source_text,
                                              source_length)
    dollar_sign_proportion = count_dollar_signs(listed_source_text,
                                                source_length)
    question_mark_proportion = count_question_marks(listed_source_text,
                                                    source_length)
    pipes_proportion = count_pipes(listed_source_text, source_length)
    percent_sign_proportion = count_percent_signs(listed_source_text,
                                                  source_length)
    at_symbol_proportion = count_at_symbols(listed_source_text, source_length)
    double_period_proportion = count_double_period(listed_source_text,
                                                   source_length)
    contains_double_plus_minus = check_double_plus_minus(listed_source_text)
    contains_colon_equals = check_colon_equals(listed_source_text)
    contains_dash_arrow = check_equals_arrow(listed_source_text)
    contains_reverse_dash_arrow = check_reverse_dash_arrow(listed_source_text)
    contains_equals_arrow = check_equals_arrow(listed_source_text)
    contains_word_function = check_for_function(listed_source_text)
    contains_word_public = check_for_public(listed_source_text)

    scores.append(comment_style)
    scores.append(print_style)
    scores.append(parentheses_proportion)
    scores.append(curly_brace_proportion)
    scores.append(double_colon_proportion)
    scores.append(semi_colon_proportion)
    scores.append(dollar_sign_proportion)
    scores.append(question_mark_proportion)
    scores.append(pipes_proportion)
    scores.append(percent_sign_proportion)
    scores.append(at_symbol_proportion)
    scores.append(contains_double_plus_minus)
    scores.append(double_period_proportion)
    scores.append(contains_colon_equals)
    scores.append(contains_dash_arrow)
    scores.append(contains_reverse_dash_arrow)
    scores.append(contains_equals_arrow)
    scores.append(contains_word_function)
    scores.append(contains_word_public)

    return np.array(scores)
