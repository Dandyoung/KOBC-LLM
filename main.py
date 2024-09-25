# main.py

import os
import json
from dotenv import load_dotenv
from utils.search import get_search_contents

def save_results_to_json(results, filename="results.json"):
    results_dict = {}
    for idx, search in enumerate(results, 1):
        key = f"result_{idx}"
        results_dict[key] = {
            "title": search["title"],
            "href": search["href"],
            "body": search["body"]
        }
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results_dict, f, ensure_ascii=False, indent=4)
        print(f"검색 결과가 '{filename}' 파일에 저장되었습니다.")
    except Exception as e:
        print(f"검색 결과를 JSON 파일로 저장하는 중 오류가 발생했습니다: {e}")

def main():
    load_dotenv()
    query = "선가정보 동향"  # 원하는 검색어로 변경 가능
    good_searches = get_search_contents(query)
    
    if good_searches:
        # 결과를 출력
        for idx, search in enumerate(good_searches, 1):
            print(f"{idx}. 제목: {search['title']}")
            print(f"   링크: {search['href']}")
            print(f"   내용: {search['body'][:400]}...\n")
        
        # JSON 파일로 저장
        save_results_to_json(good_searches, "cache/results.json")  # 원하는 파일 이름으로 변경 가능
    else:
        print("적합한 검색 결과를 찾지 못했습니다.")

if __name__ == "__main__":
    main()
