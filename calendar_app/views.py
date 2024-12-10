from django.shortcuts import render
from requests_html import AsyncHTMLSession
import asyncio

session = AsyncHTMLSession()


def index(request):
    asyncio.set_event_loop(asyncio.new_event_loop())
    results = session.run(retrieve_calendar_data)
    context = {'almost_in_season_list': retrieve_almost_in_season_list(results),
               'in_season_list': retrieve_in_season_list(results)}
    return render(request, 'greengrocer_calendar_app/index.html', context)


async def retrieve_calendar_data():
    url = "https://www.bordbia.ie/whats-in-season/best-in-season/calendar/september"
    response = await session.get(url)
    await response.html.arender()
    return response


def retrieve_almost_in_season_list(response):
    almost_in_season_container = response.html.xpath(
        '//*[@id="root"]/div/section/div[2]/div/div[9]/div[2]/div/div[1]/div/div',
        first=True)
    almost_in_season_elements = almost_in_season_container.find('h4')
    almost_in_season_list = []

    for element in almost_in_season_elements:
        almost_in_season_list.append(element.text)

    return almost_in_season_list


def retrieve_in_season_list(response):
    in_season_container = response.html.xpath(
        '//*[@id="root"]/div/section/div[2]/div/div[9]/div[2]/div/div[2]/div/div/div',
        first=True)
    in_season_elements = in_season_container.find('h4')
    in_season_list = []

    for element in in_season_elements:
        in_season_list.append(element.text)

    return in_season_list
