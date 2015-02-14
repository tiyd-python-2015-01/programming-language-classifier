import re

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
        source_lines.remove(item)
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
