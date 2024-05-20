import requests 
from bs4 import BeautifulSoup
from pathlib import Path

"""
抓取目标: 标题, 链接, 发帖人
"""

def get_html(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        # r.endcodding = r.apparent_endconding 
        r.encoding='utf-8'
        return r.text
    except Exception as e:
        print(e)
    
def get_content(url):
    """
    获取每一页的所有帖子信息
    """
    
    # 保存所有帖子信息
    comments = []
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')

    li_tags = soup.find_all('li', attrs={"class": ['j_thread_list clearfix thread_item_box']})

    for li in li_tags:
        # 使用dict存储文章信息
        comment = {}
        try:
            comment['title'] = li.find('a', attrs={"class": ['j_th_tit']}).string
            comment['link'] = "http://tieba.baidu.com/" + li.find('a', attrs={"class": ['j_th_tit']})['href']
            comment['name'] = li.find('a', attrs={"class": ['frs-author-name j_user_card']}).string
            # comment['time'] = li.find('span', attrs={"class": ['threadlist_reply_date pull_right j_reply_data']}).string
            comments.append(comment)
        except Exception as e:
            print(e)

    return comments

def out_to_file(content):
    '''
    将爬取到的文件写入到本地
    保存到当前目录的 生活大爆炸吧帖子信息.txt 文件中。

    '''
    file_path = Path("data") / "生活大爆炸吧帖子信息.txt"
    with open(file_path, 'a+', encoding='utf-8') as file:
        for comment in content:
            file.write(f"标题：{comment['title']}\t链接：{comment['link']}\t发帖ID: {comment['name']}\n")

        print('当前页面爬取完成')

def main(base_url, deep):
    url_list = []
    # 将所有需要爬去的url存入列表
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    
    print("所有链接已装载！开始筛选信息")

    for url in url_list:
        content = get_content(url)
        out_to_file(content)

    print("所有信息已写入本地文件!")


base_url = "https://tieba.baidu.com/f?ie=utf-8&kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8"
# 爬取的深度
deep = 2

if __name__ == '__main__':
    main(base_url, deep)