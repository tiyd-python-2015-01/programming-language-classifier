import requests
from bs4 import BeautifulSoup

r = requests.get('http://rosettacode.org/wiki/Category:Programming_Tasks')

soup = BeautifulSoup(r.content)

languages = [("Haskell","hs"),
             ("Clojure","clojure"),
             ("Java","java"),
             ("JavaScript","js"),
             ("OCaml","ocaml"),
             ("Perl","perl"),
             ("PHP","php"),
             ("Python","py"),
             ("Ruby","rb"),
             ("Scala","scala"),
             ("Scheme","ss"),
             ("Tcl","tcl")]

for lang, ext in languages:
    print(lang,ext)
    my_links = soup.find_all("a")
    pruned_list = my_links[7:]
    i = 1
    for link in pruned_list:
        new_link ="http://rosettacode.org{}#{}".format(link.get("href"), lang)
        #print(new_link)
        try:
            r = requests.get(new_link)
            soup1 = BeautifulSoup(r.content)
            data= soup1.find_all("pre",{"class":"{} highlighted_source".format(lang.lower())})

            for item in data:
               for tag in item.contents:
                    tag.br.replace_with("\n")
            with open("./rosetta/file{}.{}".format(i,ext), "w") as text_file:
                text_file.write(item.get_text(" "))
                i +=1
        except:
            pass
        if i ==61:
            break
