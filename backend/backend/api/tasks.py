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


def get_economic_data(checko_url: str):
    logging.info("Start get_economic_data")
    response = dict()
    page = requests.get(checko_url)
    soup = BS(page.content, "html.parser").find("article", class_="uk-flex-auto")
    s_base_info = soup.find_all("div", class_="basic-data")
    s_activity = soup.find("table", class_="uk-table uk-table-striped").find_all(
        "td", class_="uk-width-expand"
    )
    s_coeff = soup.find_all("table", class_="uk-table uk-table-small")[1].find_all("tr")

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
    logging.info("End get_economic_data")
    return response


def get_pptx_data(description: str):
    print("Start get_pptx_data")
    pptx_data = {}
    job = mlclient_lm.submit(f"qa_{description}_Кратко опиши компанию")
    pptx_data["about"] = job.result()

    job = mlclient_lm.submit(
        f"qa_{description}_Какая проблема существует на рынке компании?*Проблема: "
    )
    pptx_data["problem"] = job.result()

    job = mlclient_lm.submit(
        f"qa_{description}_Как компания решает существующие проблемы на рынке?*Для этого компания "
    )
    pptx_data["solution"] = job.result()

    job = mlclient_lm.submit(f"qa_{description}_Для кого работает компания?*Для ")
    pptx_data["target"] = job.result()

    job = mlclient_lm.submit(f"qa_{description}_В чем цель компании?*Основная цель: ")
    pptx_data["goal"] = job.result()

    job = mlclient_lm.submit(f"qa_{description}_Что делает компания?*Компания")
    pptx_data["activity"] = job.result()

    job = mlclient_lm.submit(
        f"qa_{description}_Какие преимущества у компании перед конкурентами?"
    )
    pptx_data["advantages"] = job.result()

    job = mlclient_lm.submit(
        f"qa_{description}_В чем удобство для пользователя?*Удобство для пользователя - "
    )
    pptx_data["convenience"] = job.result()

    job = mlclient_lm.submit(
        f"qa_{description}_В чем ценность и уникальность?*Главная ценность -"
    )
    pptx_data["value"] = job.result()

    print("End get_pptx_data")
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

    URL = settings.BASE_DIR / settings.MEDIA_ROOT / f"presentation-{id}.pptx"
    # driver(data, settings.BASE_DIR / f"presentation-{id}.pptx")
    print("ВСЁ ГОТОВО", URL)

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
    print("OKKKKKKK")
    presentation.result.save()

    if False:
        if presentation.checko_url is not None:
            presentation.result.pptx_data = (
                presentation.result.pptx_data
                | get_economic_data(presentation.checko_url)
            )

    presentation.result.pptx_status = "Готово"

    if False:
        if presentation.generate_logo:
            presentation.result.logo_status = "Обработка"
            presentation.result.logo = get_logo(presentation.description)
        presentation.result.logo_status = "Готово"

    presentation.result.pptx = final_generation(
        presentation.id,
        presentation.result.pptx_data,
        presentation.result.logo,
        presentation.result.name,
    )
    presentation.result.save()
