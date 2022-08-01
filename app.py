from bs4 import BeautifulSoup
from flask import Flask
from random import choice, randrange
from time import time

def parse_jokes():
    categories = [
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-6.html", "afaceri, administraţie, bani, economie"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-7.html", "bacalaureat"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-8.html", "cultură, şcoală, educaţie, maniere"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-9.html", "dragoste, căsătorie, sex, relaţii de familie"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-10.html", "filozofie, religie, istorie, gândire"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-11.html", "fotbal"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-12.html", "media"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-13.html", "muzică şi texte muzicale"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-14.html", "politică"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-15.html", "sănătate, medicină, viaţă, moarte"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-16.html", "turism, anunţuri, afişaje"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-17.html", "varia"),
        ("Radu_Paraschivescu-Noi_vorbim_nu_gandim-18.html", "respect!")
    ]

    maxime = dict()
    authors = dict()

    for src, title in categories:
        with open(f"./text/{src}", "r") as file:
            content = file.read()
            soup = BeautifulSoup(content)

            maxime[title] = []
            authors[title] = set()
            
            div = soup.find("div", {"class": "story"}).findAll("p")

            joke = ""
            for par in div[2:]:
                if par.attrs["class"][0] == "baza-x":
                    joke += par.text + "\n"
                elif par.attrs["class"][0] == "baza-x1":
                    maxime[title].append({"joke": par.text, "author": None})
                else:
                    maxime[title].append({"joke": joke, "author": par.text})
                    joke = ""
                    authors[title].add(par.text)

    return maxime, authors

def get_random_jokes():
    line_sep = 2 * "<br />" + "--------------------------------------------------------------" + 2 * "<br />"
    ret_val = "Veniți de luați stropul vostru de înțelepciune pentru ziua de astăzi!" + "<br />"

    maxime, _ = parse_jokes()
    
    ret_val += 3 * "<br />"

    for i in range(3):
        if i > 0:
            ret_val += line_sep

        title = choice(list(maxime.keys()))
        idx = randrange(len(maxime[title]))
        joke = maxime[title][idx]["joke"]
        author = maxime[title][idx]["author"]

        ret_val += joke + "<br />" + "Categorie: " + title + "<br />"
        if author is not None:
            ret_val += "Autor: " + author + "<br />"

    return ret_val

app = Flask(__name__)

last_time = 0
last_joke = ""


@app.route('/')
def update_jokes():
    global last_joke, last_time
    current_time = time()

    if current_time - last_time > 60 * 24:
        last_time = current_time
        last_joke = get_random_jokes()

    return last_joke

if __name__ == '__main__':
    app.run()