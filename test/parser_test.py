import parser


def test_read_file():
    text = parser.read_file("test/1")
    assert text


def test_split_lines():
    text = "a\nb\nc"
    text_list = parser.split_into_lines(text)
    assert text_list == ["a", "b", "c"]


def test_identify_comment_type():
    text = ["/* Test comment"]
    comment_type = parser.identify_comment_type(text)
    assert comment_type == 0

    text = ["(* Test comment *)"]
    comment_type = parser.identify_comment_type(text)
    assert comment_type == 1

    text = [";; Test comment "]
    comment_type = parser.identify_comment_type(text)
    assert comment_type == 2

    text = ["// Test comment "]
    comment_type = parser.identify_comment_type(text)
    assert comment_type == 3

    text = ["-- Test comment "]
    comment_type = parser.identify_comment_type(text)
    assert comment_type == 4

    text = ["# Test comment "]
    comment_type = parser.identify_comment_type(text)
    assert comment_type == 5


def test_identify_comment_block():
    text = ["codecode", "/* Comment", "Comment", "End */", "Code"]
    to_remove = parser.identify_comment_blocks(0, text)
    assert to_remove == ["/* Comment", "Comment", "End */"]

    text = ["codecode", "(* Comment", "Comment", "End *)", "Code"]
    to_remove = parser.identify_comment_blocks(1, text)
    assert to_remove == ["(* Comment", "Comment", "End *)"]


def test_strip_comments():
    text = ["code", "code", "/* Comment", "comment", "comment */", "code",
            "code", "// comment", "code", "// comment"]
    new_text = parser.strip_comments(0, text)
    assert new_text == ["code", "code", "code", "code", "code"]

    text = ["code", "# comment", "#comment", "code"]
    new_text = parser.strip_comments(5, text)
    assert new_text == ["code", "code"]


def test_strip_inline_comments():
    text = ["code // comment"]
    new_text = parser.strip_inline_comments(3, text)
    assert new_text == ["code "]


def test_identify_print_style():
    text = ["puts 'ths'"]
    print_type = parser.identify_print_style(text)
    assert print_type == 0

    text = ["println 'ths'"]
    print_type = parser.identify_print_style(text)
    assert print_type == 1

    text = ["printf 'ths'"]
    print_type = parser.identify_print_style(text)
    assert print_type == 2

    text = ["print 'ths'"]
    print_type = parser.identify_print_style(text)
    assert print_type == 3
