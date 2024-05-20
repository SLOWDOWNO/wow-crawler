import requests

# https://requests.readthedocs.io/en/latest/
# https://zhuanlan.zhihu.com/p/26681429

r = requests.get("http://www.baidu.com")


# print(r.headers)
"""
{'Date': 'Sun, 19 May 2024 15:50:54 GMT', 'Content-Type': 'text/html', 
'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 
'Server': 'openresty', 'Cache-Control': 'no-cache', 
'X-BILI-SEC-TOKEN': '1,denied by waf mode', 
'Set-Cookie': 'X-BILI-SEC-TOKEN=1,denied by waf mode; path=/; Expires=Sun, 19-May-24 16:20:54 GMT'}
"""

# 200
print(r.status_code)

# 访问 r.text 时要解码的编码。
# ISO-8859-1
print(r.encoding)

# utf-8
print(r.apparent_encoding)

# (property) content: bytes
print(r.content)


# requests抓取网页的通用框架
def getHTMLText(url):
    try:
        rsp = requests.get(url, timeout=30)
        # 如果状态码不是200 则应发HTTOError异常
        rsp.raise_for_status()
        # 设置正确的编码方式
        rsp.encoding = rsp.apparent_encoding
        return rsp.text
    except:
        return "getHTMLText() Error"
