"""
Небольшое Flask приложение состоящее из одной страницы.
"""
import random
import requests
import markdown
import base64
import json
import re
from opengraph_py3 import OpenGraph
from flask import Flask, render_template, request

OMDB_API_KEY = "736941b2"

URL_VALIDATOR_RE = re.compile(
    r"^((?:http(?:s)?:\/\/)?)((?:www\.)?[a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b)((?:\:\d+)?)((?:[-\w@:%\+.~#&/=]*)?)((?:\?[-\w%\+.~#&=]*)?)$"
)

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def index_handler():
    return render_template("index.html")


def movie_search_handler():
    """
    Обработчик запроса для получения и рендеринга фильмов с omdbapi
    :return список фильмов(html)
    """
    q = request.args.get("q")
    q = base64.b64decode(q).decode()
    response = requests.get(f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={q}")
    data = response.json()
    if data["Response"] == "True":
        return render_template("movies_result.html", movies=data["Search"])
    return "ERROR"


def md_handler():
    """
    Обработчик запросов для рендеринга markdown. Получает markdown из объекта запроса после чего переводит ее в HTML
    :return html полученный из markdown
    """
    q = request.args.get("q")
    q = base64.b64decode(q).decode()
    html = markdown.markdown(q)
    return html


def check_site_handler():
    """
    Обработчик запросов на проверку сайта. Прежде чем попробовать осуществить запрос проверяет корректность переданного URL.
    """
    q = request.args.get("q")
    q = base64.b64decode(q).decode()
    if not URL_VALIDATOR_RE.match(q):
        return render_template("error.html", error="Вы ввели некорректный URL")
    try:
        response = requests.get(q)
        return str(response.status_code)
    except requests.exceptions.ConnectionError:
        return render_template("error.html", error="Сайт недоступен")


@app.route("/preview")
def parse_og_handler():
    """
    Получаем информацию о странице используя Open Graph разметку на ней
    :return возвращает превью страницы (html)
    """
    q = request.args.get("q")
    q = base64.b64decode(q).decode()
    if not URL_VALIDATOR_RE.match(q):
        return render_template("error.html", error="Вы ввели некорректный URL")
    og = OpenGraph(url=q)
    return render_template("card.html", og=og)


if __name__ == "__main__":
    app.run("0.0.0.0", 8000)
