from plc.features import*

def test_character_counter():
    testcode = "This is a string with some funky characters !@*!@*(#^&!)"
    assert character_counter(testcode, 's') == 5
    assert character_counter(testcode, '!') == 3
    assert character_counter(testcode, ' ') == 8
    assert character_counter(testcode, '(') == 1

#  testcode length is 56

def test_character_ratio():
    testcode = "This is a string with some funky characters !@*!@*(#^&!)"
    assert character_ratio(testcode, ' ') == 8/56

def test_string_finder():
    test2code = ("""let min_depth = 4 let n = if Array.length
                    Sys.argv <> 2 then 0 else int_of_string Sys.argv.(1)let
                    max_depth = max (min_depth + 2) nlet stretch_depth =
                    max_depth + 1""")
    assert string_finder("let", test2code) == 4
