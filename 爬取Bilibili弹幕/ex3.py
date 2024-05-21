"""
本次爬取: https://www.bilibili.com/video/BV1qq421F7Nn/
OS: Windows 10
Vesion: Python 3.11.1 64-bit
"""

import requests
import bs4
from pathlib import Path
import csv
import pandas as pd
from wordcloud import WordCloud
import jieba

cid = "1497363064"
url = f"https://comment.bilibili.com/{cid}.xml"
headers = {
    "Refer": "https://www.bilibili.com/video/BV1sf4y1872K/?",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
}
csv_path = Path("data/csv") / "萝太永不破防_杂交版植物大战僵尸.csv"
pic_path = Path("data/img") / "萝太永不破防_杂交版植物大战僵尸词云.png"
font_path = Path("fonts") / "SanJiBangKaiJianTi-2.ttf"
stopword_file = Path("data/meta") / "cn_stopwords.txt"


def get_page(url):
    """
    获取网页内容
    """
    try:
        resp = requests.get(url, headers=headers)
        resp.encoding = resp.apparent_encoding
        print("内容已返回...")
        return resp.text
    except Exception as e:
        print(e)


def get_comments():
    """
    获取视频中所有弹幕
    """
    content = get_page(url)
    soup = bs4.BeautifulSoup(content, features="lxml")
    comments = soup.find_all("d")
    print("获取弹幕成功...")
    return comments


def write_to_csv(d_elements):
    """
    写入弹幕信息到csv文件
    """
    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["弹幕内容"])
        for d in d_elements:
            writer.writerow([d.text])
    print(f"写入到{csv_path}完成...")


def gen_worldcloud():
    """
    根据弹幕生成词云
    """
    wordcloud = WordCloud(
        width=800, height=400, background_color="white", font_path=font_path
    )
    # 读取常用中文停用词
    with open(stopword_file, "r", encoding="utf-8") as file:
        stop_words = set(file.read().splitlines())

    # 使用jieba分词
    text = []
    df = pd.read_csv(csv_path, encoding="utf-8")
    for row in df["弹幕内容"]:
        word_list = jieba.cut(row, cut_all=False)
        filtered_words = [word for word in word_list if word not in stop_words]
        text.extend(filtered_words)

    wordcloud.generate(" ".join(text))
    wordcloud.to_file(pic_path)
    print(f"词云已生成到{pic_path}...")


def main():
    print("---开始爬取弹幕---")
    comments = get_comments()
    write_to_csv(comments)
    gen_worldcloud()


if __name__ == "__main__":
    main()
