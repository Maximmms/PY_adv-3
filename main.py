import requests
import bs4

from fake_headers import Headers


## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


## Ваш код
url = 'https://habr.com/ru/articles/'
try:
    response = requests.get(url, headers=Headers(os='win', browser='chrome').generate())
except Exception as e:
    print('Ресурс недоступен, проверьте наличие подключения к сети')

soup = bs4.BeautifulSoup(response.text, 'lxml')
#получаем список статей
articles = soup.find_all('article')
for article in articles:
    relative_link = article.find('a', class_='tm-title__link')['href']
    article_link = 'https://habr.com' + relative_link
    # article_link = url + article.attrs.get('id')
    article_date = article.find('time')['datetime']
    article_header = article.find('h2').text
    #скачиваем страницу со статьёй
    response = requests.get(article_link, headers=Headers(os='win', browser='chrome').generate())
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    #получаем текст статьи
    article_body = soup.find('div', class_='tm-article-body')
    article_text = article_body.get_text().lower() if article_body else ''
    #проверяем наличие в тексте искомых слов и выводим в консоль если найдены

    if any(word.lower() in article_text for word in KEYWORDS):
        #<дата> – <заголовок> – <ссылка>
        print(f'{article_date} – {article_header} – {article_link}')