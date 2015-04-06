import pandas as pd
import os
from textblob import TextBlob


def get_tests(dir_path):
    """Pulls test files, and test key and merges them together into a df"""

    text_list = []
    ext_list = []
    for subdir, dirs, files in os.walk(dir_path):
        for name in files:
            if not name.startswith('.'):
                with open(os.path.join(subdir, name), errors="surrogateescape") as f:
                    text_list.append(f.read())
                ext_list.append(name)

    test_df = pd.DataFrame({"File number": ext_list, "Text": text_list})
    test_df["Textblob"] = test_df.Text.apply((lambda x: TextBlob(x).words))
    test_df["Textblob letters"] = test_df.Text.apply((lambda x: TextBlob(x)))
    test_df["File number"] = test_df["File number"].apply((lambda x: int(x)))
    test_df = test_df.sort("File number")

    answers = pd.read_csv("test.csv")

    test_df = pd.merge(answers, test_df,
    left_on="Filename", right_on="File number")

    test_df = test_df.drop(["Filename", "File number"], axis=1)
    
    return test_df
