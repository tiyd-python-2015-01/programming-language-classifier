from guess_lang.learner import Learner

def test_let_ratio():
    """ Test the regular expression counting 'let's
    return to a tuple and round the value to reliably test on floats. """
    code = "  let x=0"
    learner = Learner()
    name, value = learner.let_ratio(code)
    assert round(value,5) == round(1/9,5)

def test_get_ratio():
    code = "include some package"
    learner = Learner()
    name, value = learner.get_ratio(code, "include")
    assert round(value,5) == round(7/20,5)
