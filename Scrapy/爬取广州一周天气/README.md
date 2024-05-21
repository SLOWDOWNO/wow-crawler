# 爬取广州最近一周天气

爬虫框架 :  [Scrapy](https://docs.scrapy.org/en/latest/)

目标 URL : https://www.tianqi.com/guangzhou/7/

## 运行

git clone 到本地后进入 `/weater` (建项目的时候单词打错了,就不改了)
```shell
scrapy crawl GZtianqi
```

## 爬取多个城市

在 `weater/spiders/GZtianqi.py` 中

```python
class GztianqiSpider(scrapy.Spider):
    
    ...

    citys = ["guangzhou"] # 在列表中添加城市即可

    ...
```

## Reference
- https://zhuanlan.zhihu.com/p/26885412