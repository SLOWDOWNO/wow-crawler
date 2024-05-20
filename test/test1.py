import requests
import bs4
import lxml
from pathlib import Path

cid = "354066441"
url = f"https://comment.bilibili.com/{cid}.xml"
hds = {
    "Refer": "https://www.bilibili.com/video/BV1sf4y1872K/?",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
}
test_file = Path("test/data") / "test1.txt"


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


def get_comments():
    """
    获取所有弹幕
    """
    content = get_page(url)
    soup = bs4.BeautifulSoup(content, features="lxml")
    comments = soup.find_all("d")
    print("获取弹幕成功")
    return comments


def write_to_file(comments):
    """
    将弹幕写入文件
    """
    with open(test_file, "w", encoding="utf-8") as file:
        for comment in comments:
            file.write(comment.text + "\n")
    print(f"写入完成,到{test_file}查看")


def main():
    comments = get_comments()
    write_to_file(comments)


if __name__ == "__main__":
    main()
