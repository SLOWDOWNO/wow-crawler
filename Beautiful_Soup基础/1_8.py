import requests
import bs4
from pathlib import Path

"""
url: https://dianying.2345.com/top/     
爬取目标
 - 片名 + 上映时间
 - 主演
 - 简介
"""


def get_html(url):
    try:
        rsp = requests.get(url, timeout=30)
        rsp.raise_for_status()
        rsp.encoding = "gbk"
        return rsp.text
    except Exception as e:
        print(e)


def get_content(url, movies_path):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, "lxml")

    movies_list = soup.find("ul", class_="picList clearfix")
    movies = movies_list.find_all("li")

    for movie in movies:
        # 电影图片
        # img_url = movie.find('img')['src']
        # 电影名
        name = movie.find("span", class_="sTit").a.text
        try:
            # 上映时间
            time = movie.find("span", class_="sIntro").text
        except:
            time = "暂无上映时间"
        # 主演
        actors = movie.find("p", class_="pActor")
        actor = ""
        for act in actors.contents:
            actor += act.string + " "
        # 简介
        intro = movie.find("p", class_="pTxt pIntroShow").text

        with open(movies_path, "a+", encoding="utf-8") as file:
            file.write(f"片名: {name}\t {time}\n {actor}\n{intro}\n\n\n")


def main():
    url = "http://dianying.2345.com/top/"
    movies_path = Path("data/txt") / "电影排行榜信息.txt"
    get_content(url, movies_path)
    print("爬取完成")


if __name__ == "__main__":
    main()
