import os

import requests
from bs4 import BeautifulSoup


def run_code(code: str):
    response = requests.post(f"{os.environ['EWVM_URL']}/run", json={"code": code})
    html = BeautifulSoup(response.text, "html.parser")
    return "".join(element.text for element in html.find_all(class_="terminal"))
