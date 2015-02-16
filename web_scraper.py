import requests
from bs4 import BeautifulSoup
import sys

def page_scraper(scrape_page, name_of_file):
    """When given a rosetta code, code example, web page and name it
    will extract the code examples for each given language from the web page.
    Then it will create a file with the proper extension in the bench
    directory."""
    lang_dict = {"clojure": ".clojure", "haskell": ".hs", "java": ".java",
                 "javascript": ".javascript", "ocaml": ".ocaml",
                 "perl": ".pl", "php": ".php", "python": ".py",
                 "ruby": ".rb", "scala": ".scala", "scheme": ".scm"}
    file_dir = "training/benchmarks/benchmarksgame/bench/"
    page = requests.get(scrape_page)
    start_soup = BeautifulSoup(page.text)
    for lang in lang_dict.keys():
        lang_class = "pre", {"class" : lang + " highlighted_source"}
        lang_with_html = BeautifulSoup(str(start_soup(lang_class)))
        code_text = lang_with_html.get_text()
        code_text = ("").join(code_text)
        if code_text == "[]":
            pass
        else:
            parse_text = code_text[1:len(code_text) - 1]
            temp_file = open(file_dir + name_of_file + lang_dict[lang], "+w")
            temp_file.write(parse_text)
            temp_file.close()

if __name__ == "__main__":
    page = sys.argv[1]
    file = sys.argv[2]
    page_scraper(page, file)
