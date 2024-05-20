"""
爬取 bilibili 视频的弹幕
本次爬取视频为: https://www.bilibili.com/video/BV1sf4y1872K/
OS: Windows 10
"""

import csv
import pandas as pd
import jieba
from wordcloud import WordCloud
from pathlib import Path
import requests
from lxml import etree


cid = "354066441"
url = f"https://comment.bilibili.com/{cid}.xml"
csv_path = Path("data/csv") / "峰哥采访Jelly弹幕信息.csv"
pic_path = Path("data/img") / "峰哥采访Jelly弹幕词云.png"
font_path = Path("fonts") / "SanJiBangKaiJianTi-2.ttf"
stopword_file = Path("data/meta") / "cn_stopwords.txt"

hds = {
    "Refer": "https://www.bilibili.com/video/BV1sf4y1872K/?",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
}


def get_page(url):

    resp = requests.get(url, headers=hds)
    resp.encoding = "utf-8"
    # print(resp.text)
    if resp.status_code == 200:
        root = etree.fromstring(resp.content)
        d_elements = root.findall(".//d")
        print("爬取完成,开始写入文件。。。。。")
        return d_elements


def write_to_csv(d_elements):
    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["弹幕内容"])
        for d in d_elements:
            writer.writerow([d.text])
        print("写入完成")


def gen_worldcloud():
    # 读取csv文件
    df = pd.read_csv(csv_path, encoding="utf-8")
    # 词云对象
    wordcloud = WordCloud(
        width=800, height=400, background_color="white", font_path=font_path
    )

    with open(stopword_file, "r", encoding="utf-8") as file:
        stop_words = set(file.read().splitlines())  # 读取停用词并创建集合
    text = []
    # 分词
    for row in df["弹幕内容"]:
        word_list = jieba.cut(row, cut_all=False)  # 使用精确模式分词
        filtered_words = [word for word in word_list if word not in stop_words]
        text.extend(filtered_words)  # 将分词结果添加到text列表

    # 生成词云
    wordcloud.generate(" ".join(text))
    wordcloud.to_file(pic_path)
    print("词云生成完成,到data目录下查看")


if __name__ == "__main__":
    print("正在解析，开始爬取弹幕中。。。。。")
    d_elements = get_page(url)
    write_to_csv(d_elements)
    gen_worldcloud()
