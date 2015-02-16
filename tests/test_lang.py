import lang_orig1 as lang
import pandas as pd

mylist = [["for i j do na ; ;", "lang1"], ["while do never?", "lang2"]]
mylistdf = pd.DataFrame(mylist, columns = ['Code', 'Language'])

def test_join_all_code():
    assert lang.join_all_code(mylistdf) == 'for i j do na while do never'

def test_return_tokenized_data(content):
    print(lang.return_tokenized_data(content))

test_return_tokenized_data(mylistdf)
mydict={'word':'dddd','score':4}
ana = pd.DataFrame(mydict)
print(ana)
