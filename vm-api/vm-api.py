import requests
from bs4 import BeautifulSoup


def run_code(code: str):
    response = requests.post('https://ewvm.epl.di.uminho.pt/run', json={'code': code})
    html = BeautifulSoup(response.text, 'html.parser')
    return ''.join(element.text for element in html.find_all(class_='terminal'))


def main():
    code = """
pushi 1
pushi 2
add
writei
pushs "boas pessoal"
writes
    """
    print(f"'{run_code(code)}'")


if __name__ == '__main__':
    main()
