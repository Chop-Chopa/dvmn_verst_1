from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


NOW = datetime.now().year
FOUNDATION_YEAR = 1920


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def year_phrase():
    year = NOW - FOUNDATION_YEAR
    if not isinstance(year, int) or year < 0:
        raise ValueError("Число должно быть положительным целым")
    if year % 100 in (11, 12, 13, 14):
        return f"Уже {year} лет с вами"
    last_digit = year % 10
    if last_digit == 1:
        return f"Уже {year} год с вами"
    elif last_digit in (2, 3, 4):
        return f"Уже {year} года с вами"
    else:
        return f"Уже {year} лет с вами"


def load_wine_data(file_path):
    excel_data_df = pandas.read_excel(
        file_path,
        na_values=None,
        keep_default_na=False
    )
    drinks = excel_data_df.to_dict(orient='records')
    new_drinks = defaultdict(list)

    for drink in drinks:
        new_drinks[drink["Категория"]].append(drink)

    return new_drinks

categorized_drinks = load_wine_data('wine3.xlsx')

rendered_page = template.render(
    age_title=year_phrase(),
    drinkables=categorized_drinks
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
