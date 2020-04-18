import requests
from bs4 import BeautifulSoup

DATA_MAP = {
    0: "Случаев заболевания",
    1: "Случаев заболевания на текущий день",
    2: "Выздоровело",
    3: "Случаев смерти",
}

response = requests.get("https://covid.kg")
soup = BeautifulSoup(response.text, "html.parser")
elements = soup.select("div.col-md-3 .data-number")


for (idx, element) in enumerate(elements):
    print(DATA_MAP[idx] + ":", element.get_text())