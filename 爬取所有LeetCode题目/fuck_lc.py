"""
爬取LeetCode题目信息
"""

import requests
from pathlib import Path
import json


def fetch_questions(url, payload, headers):
    """获取每页的json数据,一页100条数据"""
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


def write_to_json(path, problems):
    """将json数据写入文件"""
    try:
        data_structure = {"data": {"problem_set": problems}}
        with open(path, "a", encoding="utf-8") as file:
            json.dump(data_structure, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(e)


def filter_problems(problems):
    """过滤题目信息,提取想要的数据"""

    new_data = []
    for problem in problems["data"]["problemsetQuestionList"]["questions"]:
        new_problem = {
            "pid": problem["frontendQuestionId"],
            "title": problem["title"],
            "titleCn": problem["titleCn"],
            "difficulty": problem["difficulty"],
            "url": "https://leetcode.cn/problems/" + problem["titleSlug"],
        }
        new_data.append(new_problem)
    return new_data


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Uuuserid": "c7519a0aecda3a27df1983cb8d1e5c07",
        "Referer": "https://leetcode.cn/problemset/?page=1",  # 页数
    }
    payload = {
        "operationName": "problemsetQuestionList",
        "query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    hasMore\n    total\n    questions {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId\n      isFavor\n      paidOnly\n      solutionNum\n      status\n      title\n      titleCn\n      titleSlug\n      topicTags {\n        name\n        nameTranslated\n        id\n        slug\n      }\n      extra {\n        hasVideoSolution\n        topCompanyTags {\n          imgUrl\n          slug\n          numSubscribed\n        }\n      }\n    }\n  }\n}\n    ",
        "variables": {
            "categorySlug": "all-code-essentials",
            "limit": 100,  # 每页100条数据
            "skip": 0,  # skip = (page - 1) * 100
            "filters": {},
        },
    }
    url = "https://leetcode.cn/graphql/"

    page = 1
    total_page = 3  # 最大可以爬36页

    while page <= total_page:
        output_file = Path("爬取所有LeetCode题目/data") / f"page{page}.json"
        print(f"正在爬取第{page}页数据...")

        headers["Referer"] = f"https://leetcode.cn/problemset/?page={page}"
        payload["variables"]["skip"] = (page - 1) * 100

        problems = fetch_questions(url, payload, headers)
        filtered_problems = filter_problems(problems)
        write_to_json(output_file, filtered_problems)
        page += 1

    print("爬取完成")


if __name__ == "__main__":
    main()
