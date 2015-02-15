import re

def character_counter(code, char):
    counter = 0
    for _ in code:
        if _ == char:
            counter+=1
    return counter

def character_ratio(code, char):
    value = character_counter(code, char)/len(code)
    return value

def string_finder(string, code):
    value = len(re.findall(string, code))
    return value

def string_ratio(string, code):
    value = string_finder(string, code)/len(code)
    return value

def string_end(string, code):
    if code.endswith(string):
        return 10
    else:
        return 0
