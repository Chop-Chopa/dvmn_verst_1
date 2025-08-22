from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from collections import defaultdict
import argparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


NOW = datetime.now().year
FOUNDATION_YEAR = 1920


def generate_age_phrase():
    years_count = NOW - FOUNDATION_YEAR
    if not isinstance(years_count, int) or years_count < 0:
        raise ValueError("Число должно быть положительным целым")
    if years_count % 100 in (11, 12, 13, 14):
        return f"Уже {years_count} лет с вами"
    last_digit = years_count % 10
    if last_digit == 1:
        return f"Уже {years_count} год с вами"
    elif last_digit in (2, 3, 4):
        return f"Уже {years_count} года с вами"
    else:
        return f"Уже {years_count} лет с вами"


def load_and_categorize_beverages(file_path):
    excel_data_df = pandas.read_excel(
        file_path,
        na_values=None,
        keep_default_na=False
    )
    beverages = excel_data_df.to_dict(orient='records')
    categorized_beverages = defaultdict(list)

    for beverage in beverages:
        categorized_beverages[beverage["Категория"]].append(beverage)

    return categorized_beverages


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    parser = argparse.ArgumentParser(description="Сайт с напитками")
    parser.add_argument("--data-file", default="wine_catalog.xlsx", help="Путь к Excel файлу с данными о напитках")
    args = parser.parse_args()
    
    categorized_drinks = load_and_categorize_beverages(args.data_file)

    rendered_page = template.render(
        age_title=generate_age_phrase(),
        drinkables=categorized_drinks
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
