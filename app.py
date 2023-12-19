import re
from flask import render_template, request, jsonify, redirect, request, session, g
from flask import Flask
import json

app = Flask(__name__, static_folder="static")

#  DICTIONARIES
# 1. menu_pages for the navbar
menu_pages = [
    ("Home", "/", "home"),
    ("Princess Quiz", "/princess_quiz", "princess_quiz"),
    ("About", "/about", "about"),
    ("Marvel Quiz", "/marvel_quiz", "marvel_quiz")
]
# 2. user_data for the about page
user_data = [
    ("admin", "admin", "checked")
]
# 3. questions_princess_quiz for the princess quiz
questions_princess_quiz = [ {
      "question_text": "Care este culoarea ta preferată?",
      "options": [
        {"option_text": "Albastru", "image_url": "../static/images/princess_quiz/question_1/albastru.png" , "score": {"Cinderella": 2, "Ariel": 1, "Belle": 3, "Mulan": 4, "Elsa": 1, "Rapunzel": 3, "Tiana": 2}},
        {"option_text": "Roz", "image_url": "../static/images/princess_quiz/question_1/roz.png", "score": {"Cinderella": 1, "Ariel": 3, "Belle": 2, "Mulan": 4, "Elsa": 3, "Rapunzel": 2, "Tiana": 1}},
        {"option_text": "Galben", "image_url": "../static/images/princess_quiz/question_1/galben.png", "score": {"Cinderella": 3, "Ariel": 2, "Belle": 4, "Mulan": 1, "Elsa": 4, "Rapunzel": 1, "Tiana": 2}},
        {"option_text": "Verde", "image_url": "../static/images/princess_quiz/question_1/verde.png", "score": {"Cinderella": 4, "Ariel": 1, "Belle": 3, "Mulan": 2, "Elsa": 2, "Rapunzel": 4, "Tiana": 1}}
      ]
    },
    {
      "question_text": "Ce activitate îți place cel mai mult?",
      "options": [
        {"option_text": "Cântat", "image_url": "../static/images/princess_quiz/question_2/cantat.jpg", "score": {"Cinderella": 1, "Ariel": 3, "Belle": 2, "Mulan": 4, "Elsa": 2, "Rapunzel": 3, "Tiana": 1}},
        {"option_text": "Citit", "image_url": "../static/images/princess_quiz/question_2/citit.jpg", "score": {"Cinderella": 2, "Ariel": 1, "Belle": 4, "Mulan": 3, "Elsa": 1, "Rapunzel": 2, "Tiana": 3}},
        {"option_text": "Dansat", "image_url": "../static/images/princess_quiz/question_2/dansat.jpg", "score": {"Cinderella": 4, "Ariel": 2, "Belle": 1, "Mulan": 3, "Elsa": 3, "Rapunzel": 1, "Tiana": 2}},
        {"option_text": "Gătit", "image_url": "../static/images/princess_quiz/question_2/gatit.jpg", "score": {"Cinderella": 3, "Ariel": 1, "Belle": 2, "Mulan": 4, "Elsa": 4, "Rapunzel": 2, "Tiana": 3}}
      ]
    },
    {
      "question_text": "Care este locul tău preferat pentru vacanță?",
      "options": [
        {"option_text": "Plajă exotică", "image_url": "../static/images/princess_quiz/question_3/plaja_exotica.jpg", "score": {"Cinderella": 1, "Ariel": 3, "Belle": 2, "Mulan": 4, "Elsa": 4, "Rapunzel": 1, "Tiana": 2}},
        {"option_text": "Munte", "image_url": "../static/images/princess_quiz/question_3/munte.jpg", "score": {"Cinderella": 2, "Ariel": 1, "Belle": 4, "Mulan": 3, "Elsa": 2, "Rapunzel": 3, "Tiana": 1}},
        {"option_text": "Oraș aglomerat", "image_url": "../static/images/princess_quiz/question_3/oras_aglomerat.jpg", "score": {"Cinderella": 4, "Ariel": 2, "Belle": 1, "Mulan": 3, "Elsa": 3, "Rapunzel": 2, "Tiana": 4}},
        {"option_text": "Sat liniștit", "image_url": "../static/images/princess_quiz/question_3/sat_linistit.jpg", "score": {"Cinderella": 3, "Ariel": 1, "Belle": 2, "Mulan": 4, "Elsa": 1, "Rapunzel": 4, "Tiana": 3}}
      ]
    },
    {
      "question_text": "Ce fel de muzică îți place cel mai mult?",
      "options": [
        {"option_text": "Pop", "image_url": "../static/images/princess_quiz/question_4/muzica_pop.jpg", "score": {"Cinderella": 1, "Ariel": 3, "Belle": 2, "Mulan": 4, "Elsa": 2, "Rapunzel": 3, "Tiana": 1}},
        {"option_text": "Rock", "image_url": "../static/images/princess_quiz/question_4/muzica_rock.jpg", "score": {"Cinderella": 2, "Ariel": 1, "Belle": 4, "Mulan": 3, "Elsa": 1, "Rapunzel": 2, "Tiana": 3}},
        {"option_text": "Clasică", "image_url": "../static/images/princess_quiz/question_4/muzica_clasica.jpg", "score": {"Cinderella": 4, "Ariel": 2, "Belle": 1, "Mulan": 3, "Elsa": 3, "Rapunzel": 1, "Tiana": 2}},
        {"option_text": "Jazz", "image_url": "../static/images/princess_quiz/question_4/muzica_jazz.jpg", "score": {"Cinderella": 3, "Ariel": 1, "Belle": 2, "Mulan": 4, "Elsa": 4, "Rapunzel": 2, "Tiana": 3}}
      ]
    },
    {
      "question_text": "Ce superputere ai vrea să ai?",
      "options": [
        {"option_text": "Invizibilitate", "image_url": "../static/images/princess_quiz/question_5/invizibilitate.jpg", "score": {"Cinderella": 1, "Ariel": 3, "Belle": 2, "Mulan": 4, "Elsa": 4, "Rapunzel": 1, "Tiana": 2}},
        {"option_text": "Zbor", "image_url": "../static/images/princess_quiz/question_5/zbor.jpg", "score": {"Cinderella": 2, "Ariel": 1, "Belle": 4, "Mulan": 3, "Elsa": 2, "Rapunzel": 3, "Tiana": 1}},
        {"option_text": "Superforță", "image_url": "../static/images/princess_quiz/question_5/superforta.jpg", "score": {"Cinderella": 4, "Ariel": 2, "Belle": 1, "Mulan": 3, "Elsa": 3, "Rapunzel": 2, "Tiana": 4}},
        {"option_text": "Teleportare", "image_url": "../static/images/princess_quiz/question_5/teleportare.jpg", "score": {"Cinderella": 3, "Ariel": 1, "Belle": 2, "Mulan": 4, "Elsa": 1, "Rapunzel": 4, "Tiana": 3}}
      ]
    },
    {
      "question_text": "Ce tip de film îți place să vezi?",
      "options": [
        {"option_text": "Dramă", "image_url": "../static/images/princess_quiz/question_6/drama.jpg", "score": {"Cinderella": 1, "Ariel": 3, "Belle": 2, "Mulan": 4, "Elsa": 2, "Rapunzel": 3, "Tiana": 1}},
        {"option_text": "Comedie", "image_url": "../static/images/princess_quiz/question_6/comedie.jpg", "score": {"Cinderella": 2, "Ariel": 1, "Belle": 4, "Mulan": 3, "Elsa": 1, "Rapunzel": 2, "Tiana": 3}},
        {"option_text": "Aventură", "image_url": "../static/images/princess_quiz/question_6/aventura.jpg", "score": {"Cinderella": 4, "Ariel": 2, "Belle": 1, "Mulan": 3, "Elsa": 3, "Rapunzel": 1, "Tiana": 2}},
        {"option_text": "SF", "image_url": "../static/images/princess_quiz/question_6/SF.jpg", "score": {"Cinderella": 3, "Ariel": 1, "Belle": 2, "Mulan": 4, "Elsa": 4, "Rapunzel": 2, "Tiana": 3}}
      ]
    },
    {
      "question_text": "Ce ai face într-o zi ploioasă?",
      "options": [
        {"option_text": "Citit o carte", "image_url": "../static/images/princess_quiz/question_7/citit_o_carte.jpg", "score": {"Cinderella": 1, "Ariel": 3, "Belle": 2, "Mulan": 4, "Elsa": 4, "Rapunzel": 1, "Tiana": 2}},
        {"option_text": "Uitat la ploaie", "image_url": "../static/images/princess_quiz/question_7/uitat_la_ploaie.jpg", "score": {"Cinderella": 2, "Ariel": 1, "Belle": 4, "Mulan": 3, "Elsa": 2, "Rapunzel": 3, "Tiana": 1}},
        {"option_text": "Făcut un puzzle", "image_url": "../static/images/princess_quiz/question_7/facut_un_puzzle.jpg", "score": {"Cinderella": 4, "Ariel": 2, "Belle": 1, "Mulan": 3, "Elsa": 3, "Rapunzel": 2, "Tiana": 4}},
        {"option_text": "Gătit ceva bun", "image_url": "../static/images/princess_quiz/question_7/gatit_ceva_bun.jpg", "score": {"Cinderella": 3, "Ariel": 1, "Belle": 2, "Mulan": 4, "Elsa": 1, "Rapunzel": 4, "Tiana": 3}}
      ]
    }
]
# 4. description for the princess quiz results
description_princess_quiz = {
  "Cinderella" : {"description": "Ești o persoană foarte ambițioasă și nu te lași până nu obții ceea ce îți dorești. Ești o persoană foarte bună și îți place să ajuți pe cei din jurul tău. Ești o persoană foarte curajoasă și nu te lași până nu îți atingi obiectivele."},
  "Ariel" : {"description": "Ești o persoană foarte curioasă și îți place să încerci lucruri noi. Ești o persoană foarte sensibilă și îți pasă foarte mult de cei din jurul tău. Ești o persoană foarte creativă și îți place să îți exprimi sentimentele prin artă."},
  "Belle" : {"description": "Ești o persoană foarte inteligentă și îți place să înveți lucruri noi. Ești o persoană foarte curajoasă și îți place să încerci lucruri noi. Ești o persoană foarte ambițioasă și nu te lași până nu îți atingi obiectivele."},
  "Mulan" : {"description": "Ești o persoană foarte curajoasă și îți place să încerci lucruri noi. Ești o persoană foarte ambițioasă și nu te lași până nu îți atingi obiectivele. Ești o persoană foarte inteligentă și îți place să înveți lucruri noi."},
  "Elsa" : {"description": "Ești o persoană foarte creativă și îți place să îți exprimi sentimentele prin artă. Ești o persoană foarte sensibilă și îți pasă foarte mult de cei din jurul tău. Ești o persoană foarte inteligentă și îți place să înveți lucruri noi."},
  "Rapunzel" : {"description": "Ești o persoană foarte creativă și îți place să îți exprimi sentimentele prin artă. Ești o persoană foarte sensibilă și îți pasă foarte mult de cei din jurul tău. Ești o persoană foarte curioasă și îți place să încerci lucruri noi."},
  "Tiana" : {"description": "Ești o persoană foarte ambițioasă și nu te lași până nu îți atingi obiectivele. Ești o persoană foarte curajoasă și îți place să încerci lucruri noi. Ești o persoană foarte inteligentă și îți place să înveți lucruri noi."}
}
# 5. questions_marvel_quiz for the marvel quiz
questions_marvel_quiz = [
    {
        "question_text": "Care supererou Marvel îți place cel mai mult?",
        "options": [
            {"option_text": "Iron Man", "score": {"Iron Man": 4, "Spider-Man": 2, "Captain America": 1, "Thor": 3}},
            {"option_text": "Spider-Man", "score": {"Iron Man": 2, "Spider-Man": 4, "Captain America": 3, "Thor": 1}},
            {"option_text": "Captain America", "score": {"Iron Man": 1, "Spider-Man": 3, "Captain America": 4, "Thor": 2}},
            {"option_text": "Thor", "score": {"Iron Man": 3, "Spider-Man": 1, "Captain America": 2, "Thor": 4}}
        ]
    },
    {
        "question_text": "Care superputere ți-ar plăcea să o ai?",
        "options": [
            {"option_text": "Zbor", "score": {"Iron Man": 3, "Spider-Man": 2, "Captain America": 1, "Thor": 4}},
            {"option_text": "Aranjare de păianjen", "score": {"Iron Man": 2, "Spider-Man": 4, "Captain America": 1, "Thor": 3}},
            {"option_text": "Super putere fizică", "score": {"Iron Man": 1, "Spider-Man": 2, "Captain America": 4, "Thor": 3}},
            {"option_text": "Manipulare a elementelor", "score": {"Iron Man": 4, "Spider-Man": 1, "Captain America": 2, "Thor": 3}}
        ]
    },
    {
        "question_text": "Care antagonist Marvel îți place cel mai mult?",
        "options": [
            {"option_text": "Loki", "score": {"Iron Man": 2, "Spider-Man": 3, "Captain America": 1, "Thor": 4}},
            {"option_text": "Green Goblin", "score": {"Iron Man": 1, "Spider-Man": 4, "Captain America": 2, "Thor": 3}},
            {"option_text": "Red Skull", "score": {"Iron Man": 3, "Spider-Man": 2, "Captain America": 4, "Thor": 1}},
            {"option_text": "Thanos", "score": {"Iron Man": 4, "Spider-Man": 1, "Captain America": 3, "Thor": 2}}
        ]
    }
]
# 6. Informații despre supereroi Marvel
marvel_hero_info = {
    "Iron Man": {"description": "Iron Man este un inventator genial și om de afaceri, echipat cu o armură puternică."},
    "Spider-Man": {"description": "Spider-Man este un tânăr erou cu abilități de a se deplasa pe pereți și lansa pânze de păianjen."},
    "Captain America": {"description": "Captain America este un super-soldat cu o scută indestructibilă și abilități fizice îmbunătățite."},
    "Thor": {"description": "Thor este zeul norvegian al tunetului și fulgerului, echipat cu un ciocan magic numit Mjolnir."}
}
@app.before_request
def init_menu():
    g.menu_pages = menu_pages
    g.user_data = user_data
    g.questions_princess_quiz = questions_princess_quiz
    g.questions_marvel_quiz = questions_marvel_quiz
    # g.scores = scores

@app.route("/")
def home():
    return render_template("index.html", active_page="home")

@app.route("/princess_quiz", methods=["GET", "POST"])
def princess_quiz():
  global scores
  scores = {"Cinderella": 0, "Ariel": 0, "Belle": 0, "Mulan": 0, "Elsa": 0, "Rapunzel": 0, "Tiana": 0}
  if request.method == "POST":
  # vreau sa arata toate rapunsurile posibile din form
    for i, question in enumerate(questions_princess_quiz):
        selected_answer = request.form.get(f"question_{i}")
        print(f"Răspunsul selectat pentru întrebarea {i} este: {selected_answer}")
        if selected_answer:
            for option in question["options"]:
                if option["option_text"] == selected_answer:
                    for character, score in option["score"].items():
                        scores[character] += score
    # print(scores)
    max_princess = max(scores, key=scores.get)
    max_princess_description = description_princess_quiz[max_princess]["description"]
    if scores[max_princess] == 0:
      return render_template("princess_quiz_results.html", active_page="princess_quiz", scores=scores, max_princess="Nimeni", max_princess_description="Nu ai răspuns la nicio întrebare.")
    return render_template("princess_quiz_results.html", active_page="princess_quiz", scores=scores, max_princess=max_princess, max_princess_description=max_princess_description)
  return render_template("princess_quiz.html", active_page="princess_quiz", questions=g.questions_princess_quiz)
  # return render_template("princess_quiz_results.html", active_page="princess_quiz", scores=scores)

@app.route("/princess_quiz_result", methods=["POST"])
def princess_quiz_results():
  return render_template("princess_quiz_results.html", active_page="princess_quiz")

@app.route("/about", methods=["POST", "GET"])
def about():
    email = request.form.get("email")
    password = request.form.get("password")
    checked = request.form.get("checkbox")
    range_value = request.form.get("rangeInput")
    print(email, password, checked, range_value)
    if checked == "on":
        g.user_data.append((email, password, checked))
        print(g.user_data)
    else:
        print("unchecked")
    return render_template("about.html", active_page="about")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)