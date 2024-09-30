# main.py

import os
import json
from dotenv import load_dotenv
from utils.search import get_search_contents

def save_results_to_json(results, filename="cache/results.json"):
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
        print(f"저장 중 오류 발생 : {e}")


#근 2년간의 데이터로 전처리하는 함수
'''
이부분 모듈로 뺴야함 
'''
def data_preprocessing(file_path) :

    import pandas as pd
    df = pd.read_excel(file_path, skiprows=1, engine='xlrd')
    df = df.drop(columns=['번호'])
    df = df.set_index('DATE')
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

    # 조건에 맞는 데이터 필터링 (괄호와 비트 연산자 사용)
    filtered_df = df.loc[
        (df.index > '2022-06-01') & (df.index < '2024-06-30')
    ]
    # 일단 단위를 맞추기 위해서 100 추가
    filtered_df = filtered_df + 100
    return filtered_df

def main():
    load_dotenv()
    query = "2년간 벌크선의 신조선가 동향에 대해 설명해주세요"  # 원하는 검색어로 변경 가능 (현재 키워드 추출은 불가)
    good_searches = get_search_contents(query)
    bulker_xlsx = "/workspace/youngwoo/KOBCLLM/resource/신조선가/BULKER.xls"
    bulker_df = data_preprocessing(bulker_xlsx)

    if good_searches:
        # 결과를 출력
        for idx, search in enumerate(good_searches, 1):
            print(f"{idx}. 제목: {search['title']}")
            print(f"   링크: {search['href']}")
            print(f"   내용: {search['body'][:400]}...\n")
        
        # JSON 파일로 저장
        save_results_to_json(good_searches, "cache/results.json")  # 원하는 파일 이름으로 변경 가능
    
        try:
            with open("cache/results.json", "r", encoding="utf-8") as f:
                results_dict = json.load(f)
            
            # 'body' 내용 추출 및 결합
            bodies = []
            for key in results_dict:
                body_content = results_dict[key]['body']
                bodies.append(body_content)
            reference = "\n".join(bodies)
        except Exception as e:
            print(f"JSON 파일을 읽는 중 오류가 발생했습니다: {e}")
            reference = ""

        # 입력 텍스트 생성
        MESSAGE = query
        REFERENCE = reference
        DATAFRAME = bulker_df

        '''
        이부분 모듈로 뺴야함 
        '''
        input_text = f"""당신은 데이터 분석 전문가입니다.
        사용자 요청에 답변하기 위한 뉴스기사 및 추가 정보를 제공해드리겠습니다.
        해당 정보들을 활용해 답변하세요.

        # 사용자 요청
        {MESSAGE}

        # 사용자의 요청에 따라 데이터베이스에서 추출한 데이터
        {DATAFRAME}

        # 사용자 요청과 관련있는 뉴스 기사
        {REFERENCE}

        **참고사항:**
        - 신조선가 지수(newbuilding price index)는 88년 1월의 선가를 100으로 산출한 지수이며, 88년 1월보다 얼마나 상승했는지를 나타냅니다.
        - 신조선가 지수 단위는 pt입니다.
        - 숫자 언급 시, 소수점 두 자리까지 표기하세요.
        - 분석 내용은 객관적이고 명확하게 작성하세요.
        - 반드시 동일 연도, 월을 구체적인 %, pt 수치를 언급하며 비교하세요.
        - 반드시 상승/하강 원인을 분석하고, 향후 전망을 제시해 주세요.
        - 반드시 추가적인 배경 정보나 관련 트렌드를 포함해주세요.
        """

        # print("\n=== 입력 텍스트 ===\n")
        print(input_text)

        messages = [
            {"role": "user", "content":input_text},
        ]

        # print(messages[0])
        '''
        이부분 모듈로 뺴야함 
        '''
        import torch
        from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
        from utils.model import model, tokenizer

        # 파이프라인 설정
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device="cuda",  # replace with "mps" to run on a Mac device
        )

        # # 응답 생성
        # outputs = pipe(
        #     input_text,
        #     max_new_tokens=500,
        #     do_sample=True,
        #     temperature=0.7,
        #     top_p=0.9,
        #     repetition_penalty=1.1,
        #     eos_token_id=tokenizer.eos_token_id,
        # )

        outputs = pipe(messages, max_new_tokens=5000)
        assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
        print(assistant_response)

    else:
        print("적합한 검색 결과를 찾지 못했습니다.")

if __name__ == "__main__":
    main()
