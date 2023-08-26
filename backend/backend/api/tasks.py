import logging

import requests
from bs4 import BeautifulSoup as BS

from backend.api.models import Presentation
from backend.celery import celery_app


def get_economic_data(checko_url: str):
    logging.info("Start get_economic_data")
    response = dict()
    page = requests.get(checko_url)
    soup = BS(page.content, "html.parser").find("article", class_="uk-flex-auto")
    s_base_info = soup.find_all("div", class_="basic-data")
    s_activity = soup.find("table", class_="uk-table uk-table-striped").find_all("td", class_="uk-width-expand")
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
    return {"Задача": "Заработать миллион"}


def get_logo(description: str):
    return "https://cdn.logo.com/hotlink-ok/logo-social.png"


def get_name(description: str):
    return "Моя презентация"


def final_generation(pptx_data: dict, logo: str, name: str):
    return "https://cdn.logo.com/hotlink-ok/logo-social.png"


@celery_app.task(bind=True)
def process_presentation(self, presentation_id: int):
    presentation = Presentation.objects.get(pk=presentation_id)
    if presentation.generate_name:
        presentation.result.name = get_name(presentation.description)
    presentation.result.pptx_data = get_pptx_data(presentation.description)
    if presentation.checko_url != "":
        presentation.result.pptx_data = presentation.result.pptx_data | get_economic_data(presentation.checko_url)
    if presentation.generate_logo:
        presentation.result.logo = get_logo(presentation.description)
    presentation.result.pptx = final_generation(presentation.result.pptx_data, presentation.result.logo, presentation.result.name)
