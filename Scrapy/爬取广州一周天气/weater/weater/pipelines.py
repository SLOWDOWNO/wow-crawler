# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import requests
import json
import codecs
import pymysql


class WeaterPipeline:
    def process_item(self, item, spider):
        """处理每个从GZtianqi传过来的item"""

        # 获取当前工作目录
        base_dir = os.getcwd()
        file_path = base_dir + "/data/weather.txt"

        # 写入文件
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(
                f"{item['date']}\r{item['week']}\r{item['temperature']}\r{item['weather']}\r\n"
            )

        # 下载图片
        with open(base_dir + "/data/" + item["date"] + ".png", "wb") as file:
            headers = {
                "Referer": "https://www.tianqi.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            }
            response = requests.get(item["img"], headers=headers)
            file.write(response.content)

        return item

        # print("--------------------")
        # print(type(item["date"]))
        # print(type(item["week"]))
        # print(type(item["temperature"]))
        # print(type(item["weather"]))
        # print(item["img"])
        # print("--------------------")


class Write2Json:
    def process_item(self, item, spider):
        """
        将爬取的信息保存到json
        方便其他程序员调用
        """

        base_dir = os.getcwd()
        file_path = base_dir + "/data/weather.json"

        # 打开json文件，向里面以dumps的方式吸入数据
        with codecs.open(file_path, "a", encoding="utf-8") as file:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            file.write(line)

        return item


class Write2MySQL:
    def process_item(self, item, spider):
        """
        将爬取的信息保存到mysql
        """
        date = item["date"]
        week = item["week"]
        temperature = item["temperature"]
        weather = item["weather"]
        img = item["img"]

        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            db="scrapydb",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        try:
            with conn.cursor() as cursor:
                sql = """insert into weather(date, week, temperature, weather, img) values(%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (date, week, temperature, weather, img))

            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

        return item
