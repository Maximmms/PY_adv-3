import requests
import bs4

from fake_headers import Headers


## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


## Ваш код
url = 'https://habr.com/ru/articles/'
response = requests.get(url, headers=Headers(os='win', browser='chrome').generate())

soup = bs4.BeautifulSoup(response.text, 'lxml')
#получаем список статей
articles = soup.find_all('article')
for article in articles:
    article_link = url + article.attrs.get('id')
    article_date = article.find('time')['datetime']
    article_header = article.find('h2').text
    #скачиваем страницу со статьёй
    response = requests.get(article_link, headers=Headers(os='win', browser='chrome').generate())
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    #получаем текст статьи
    article_text = soup.find('div', attrs={'xmlns': 'http://www.w3.org/1999/xhtml'})
    #проверяем наличие в тексте искомых слов и выводим в консоль если найдены
    for paragraph in article_text:
        if any(word in paragraph.text for word in KEYWORDS):
            #<дата> – <заголовок> – <ссылка>
            print(f'{article_date} – {article_header} – {article_link}')
            break