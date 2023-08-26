import logging

import requests
from bs4 import BeautifulSoup as BS

from backend.api.models import Presentation
from backend.celery import celery_app, mlclient_lm
from pprint import pprint
from copy import deepcopy
from django.conf import settings

from backend.presentations.generation import driver

BASE_DATA = {
    "bg": {
        "type": "gradient",
        "color1": "a3fff9",
        "color2": "a3b4ff",
        "angle": 45,
    },
    "logo": {"size": 0.7, "path": "logo.png"},
    "font": {"name": "VK Sans Display", "title_size": 50, "regular_size": 38},
}


def get_economic_data(inn: str):
    logging.info("Start get_economic_data")
    response = dict()
    page = requests.get(f"https://checko.ru/search?query={inn}")
    soup = BS(page.content, "html.parser").find("article", class_="uk-flex-auto")
    s_base_info = soup.find_all("div", class_="basic-data")
    s_activity = soup.find("table", class_="uk-table uk-table-striped").find_all("td", class_="uk-width-expand")
    s_coeff = soup.find_all("table", class_="uk-table uk-table-small")[1].find_all("tr")
    s_competitors = soup.find("table", class_="uk-table data-table no-last-border")

    response["date_registration"] = s_base_info[2].find_all("div")[1].text
    response["legal_address"] = s_base_info[4].find_all("div")[1].text
    response["legal_address"] = s_base_info[4].find_all("div")[1].text

    response["activity"] = [i.text.replace("?", "") for i in s_activity]

    response["coeff_autonomy"] = s_coeff[1].text.split()[-1]
    response["coeff_availability_own_capital"] = s_coeff[2].text.split()[-1]
    response["investment_coverage_ratio"] = s_coeff[3].text.split()[-1]

    response["current_liquidity_ratio"] = s_coeff[5].text.split()[-1]
    response["quick_liquidity_ratio"] = s_coeff[6].text.split()[-1]
    response["absolute_liquidity_ratio"] = s_coeff[7].text.split()[-1]

    response["return_sales"] = s_coeff[9].text.split()[-1]
    response["return_assets"] = s_coeff[10].text.split()[-1]
    response["return_equity"] = s_coeff[11].text.split()[-1]

    response["competitors"] = [i.text for i in s_competitors.find_all("a", class_="link")]
    logging.info("End get_economic_data")
    return response


def get_pptx_data(description: str):
    keys = {
        "about": f"qa_{description}_Кратко опиши компанию",
        "problem": f"qa_{description}_Какая проблема существует на рынке компании?*Проблема: ",
        "solution": f"qa_{description}_Как компания решает существующие проблемы на рынке?*Для этого компания ",
        "target": f"qa_{description}_Для кого работает компания?*Для ",
        "goal": f"qa_{description}_В чем цель компании?*Цель компании ",
        "activity": f"qa_{description}_Что делает компания?*Компания",
        "advantages": f"qa_{description}_Какие преимущества у компании перед конкурентами?*Преимущества: ",
        "convenience": f"qa_{description}_В чем удобство для пользователя?*Удобство для пользователя - ",
        "value": f"qa_{description}_В чем ценность и уникальность?*Главная ценность -",
    }

    # print("Start get_pptx_data")
    # pptx_data = {}
    # for key, value in keys.items():
    #     pptx_data[key] = mlclient_lm.submit(value).result()
    # print("End get_pptx_data")

    pptx_data = {
        "about": "Описание: Приложение для запоминания математических формул",
        "problem": "Проблема: Приложение для запоминания математических формул",
        "solution": "Для этого компания Приложение для запоминания математических формул",
        "target": "Для Приложение для запоминания математических формул",
        "goal": "Основная цель: Приложение для запоминания математических формул",
        "activity": "Компания Приложение для запоминания математических формул",
        "advantages": "Приложение для запоминания математических формул",
        "convenience": "Удобство для пользователя - Приложение для запоминания математических формул",
        "value": "Главная ценность - Приложение для запоминания математических формул",
    }

    return pptx_data


def get_logo(description: str):
    return "https://cdn.logo.com/hotlink-ok/logo-social.png"


def get_name(description: str):
    job = mlclient_lm.submit(f"tg_{description}")
    return job.result()


def final_generation(id: int, pptx_data: dict, logo: str, name: str):
    data = deepcopy(BASE_DATA)
    data["name"] = name
    data["brief"] = pptx_data["about"]

    FILENAME = f"media/presentation-{id}.pptx"
    URL = str(settings.BASE_DIR / FILENAME)

    driver(data, URL)

    return URL


@celery_app.task(bind=True)
def process_presentation(self, presentation_id: int):
    presentation = Presentation.objects.get(pk=presentation_id)

    if presentation.generate_name:
        presentation.result.name_status = "Обработка"
        presentation.result.name = get_name(presentation.description)
    presentation.result.name_status = "Готово"

    presentation.result.pptx_status = "Обработка"
    presentation.result.pptx_data = get_pptx_data(presentation.description)
    if presentation.checko_url is not None:
        presentation.result.pptx_data = (
            presentation.result.pptx_data | get_economic_data(presentation.checko_url)
        )
    presentation.result.pptx_status = "Готово"

    if presentation.generate_logo:
        presentation.result.logo_status = "Обработка"
        presentation.result.logo = get_logo(presentation.description)
    presentation.result.logo_status = "Готово"

    presentation.result.pptx = final_generation(
        presentation.id,
        presentation.result.pptx_data,
        presentation.result.logo,
        "MathUp",
    )
    presentation.result.save()
