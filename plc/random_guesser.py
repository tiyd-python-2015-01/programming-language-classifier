import random

def random_guesser(y_test):
    lang_list = ['clojure', 'python', 'javascript', 'ruby', 'haskell', 'scheme', 'java', 'scala', 'php', 'ocaml']
    correct_count = 0
    total_count = 0
    for answer in y_test:
        if answer == random.choice(lang_list):
            correct_count+=1
            total_count+=1
        else:
            total_count+=1
    return correct_count/total_count


def average_of_random_guesser(y_test, number):
    alist = []
    for num in range(number):
        alist.append(random_guesser(y_test))
    x = sum(alist)/len(alist)
    return x


def max_of_random_guesser(y_test, number):
    alist = []
    for num in range(number):
        alist.append(random_guesser(y_test))
    x = max(alist)
    return x
