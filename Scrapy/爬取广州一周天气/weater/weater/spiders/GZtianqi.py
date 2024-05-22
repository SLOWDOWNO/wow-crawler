import scrapy
from weater.items import WeaterItem


class GztianqiSpider(scrapy.Spider):
    name = "GZtianqi"
    allowed_domains = ["tianqi.com"]

    # start_urls = ["https://tianqi.com/guangzhou/7/"]
    start_urls = []

    citys = ["guangzhou"]

    for city in citys:
        start_urls.append(f"https://www.tianqi.com/{city}/7/")

    def parse(self, response):
        """筛选信息的函数
        date = 几月几号
        week = 今天、明天、后天、星期X
        temperature = 当天温度
        weather = 天气
        """

        # 保存每天的信息
        items = []

        # 找到包裹着每天天气信息的<ul class="weaul">,里面嵌套的li标签就是每天的信息
        severn_days = response.xpath('//ul[@class="weaul"]/li')

        # 筛选每天的信息
        for index, day in enumerate(severn_days, start=1):

            item = WeaterItem()

            if index <= 3:
                item["date"] = day.xpath(
                    "./a/div[@class='weaul_q weaul_qblue']/span[@class='fl']/text()"
                )[0].extract()
                item["week"] = day.xpath(
                    "./a/div[@class='weaul_q weaul_qblue']/span[@class='fr']/text()"
                )[0].extract()
            else:
                item["date"] = day.xpath(
                    "./a/div[@class='weaul_q']/span[@class='fl']/text()"
                )[0].extract()
                item["week"] = day.xpath(
                    "./a/div[@class='weaul_q']/span[@class='fr']/text()"
                )[0].extract()

            left = day.xpath("./a/div[4]/span[1]/text()")[0]
            right = day.xpath("./a/div[4]/span[2]/text()")[0]
            item["temperature"] = f"{left} ~ {right} ℃"

            item["img"] = "https:" + day.xpath("./a/div[2]/img/@src")[0].extract()
            item["weather"] = day.xpath("./a/div[3]/text()")[0].extract()
            items.append(item)

        return items
