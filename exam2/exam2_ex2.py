import requests
from bs4 import BeautifulSoup as bs

rt_base_link = "https://www.company.rt.ru"
news_base_link = f'{rt_base_link}/press/?PAGEN='

news_list = []
page_num = 0

while len(news_list) < 20:
    page_num += 1
    paged_link = f'{news_base_link}{page_num}'
    response = requests.get(f'{news_base_link}{page_num}')
    soup = bs(response.text, "html.parser")
    news = soup.find_all("div", class_="item news_item item--covered", limit=20)
    for new in news:
        new_item_link = new.find("a", class_="item_link").get("href")
        full_new_item_link = f'{rt_base_link}{new_item_link}'

        news_day = new.find("span", class_="item_date-day").text
        news_month = new.find("span", class_="item_date-month").text
        full_new_item_date = f'{news_day} {news_month}'

        news_title = new.find("div", class_="item_text").text

        news_list.append({'date': full_new_item_date, 'title': news_title, 'link': full_new_item_link})
        if len(news_list) == 20:
            break

for news in news_list:
    print(news.get('title'))
    print(f'\t{news.get('date')}')
    print(f'\t{news.get('link')}')
    print()
