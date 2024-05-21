import requests
import bs4
from lxml import etree
from pathlib import Path


url = "https://www.tianqi.com/changchun/7/"
hds = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}


def get_page(url):
    """
    获取网页内容
    """
    try:
        resp = requests.get(url, headers=hds)
        resp.encoding = resp.apparent_encoding
        print("内容已返回")
        return resp.text
    except Exception as e:
        print(e)


def main():
    page = get_page(url)
    html = etree.HTML(page)

    days = html.xpath("//ul[@class='weaul']/li")

    for index, day in enumerate(days, start=1):
        if index <= 3:
            date = day.xpath(
                "./a/div[@class='weaul_q weaul_qblue']/span[@class='fl']/text()"
            )[0]
            week = day.xpath(
                "./a/div[@class='weaul_q weaul_qblue']/span[@class='fr']/text()"
            )[0]
        else:
            date = day.xpath("./a/div[@class='weaul_q']/span[@class='fl']/text()")[0]
            week = day.xpath("./a/div[@class='weaul_q']/span[@class='fr']/text()")[0]

        left = day.xpath("./a/div[4]/span[1]/text()")[0]
        right = day.xpath("./a/div[4]/span[2]/text()")[0]
        temperature = f"{left} ~ {right} ℃"

        weather = day.xpath("./a/div[3]/text()")[0]

        half_url = day.xpath("./a/div[2]/img/@src")[0]
        print(date, week, temperature, weather, half_url)


if __name__ == "__main__":
    main()
