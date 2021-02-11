import requests

from bs4 import BeautifulSoup


class FunpaySplitParser(object):

    data = ()
    url = None

    def __init__(self, url, *keywords):
        self.url = f"{url}?desc={'+'.join(keywords)}#"

    def parse(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')
        products = soup.select("a.tc-item")

        for product in products:
            description = product.select_one("div.tc-desc-text").text.strip()
            price = product.select_one("div.tc-price").text.strip()

            media_user_name = product.select_one("div.media-user-name")

            user_name = media_user_name.text.strip()
            user_reviews = product.select_one("div.media-user-reviews").text.strip()
            user_registration = product.select_one("div.media-user-info").text.strip()
            user_href = media_user_name.find("span").get("data-href")

            href = product.get("href")

            result = {
                'description': description,
                'price': float(price.replace(' ', '')[:-1]),

                'user_name': user_name,
                'user_reviews': int(user_reviews.split(' ')[0].replace('нет', '0')),
                'user_registration': user_registration,
                'user_href': user_href,

                'href': href,
            }

            print(result)
            yield result


def formatter():
    with open("next.txt", "r") as base:

        with open("base.txt", "w") as new:

            for line in base.readlines():
                login_data = line.split(' ')[0]

                if len(login_data) > 1:
                    new.write(login_data + '\n')


if __name__ == "__main__":
    parser = FunpaySplitParser(url="https://funpay.ru/lots/157/")
    print(len(tuple(parser.parse())))
