from transformers import AutoTokenizer, AutoModelForCausalLM
from config import MODEL_NAME, CACHE_DIR
import torch

# 모델 로드
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2-9b-it", 
    torch_dtype=torch.bfloat16, 
    cache_dir="/workspace/youngwoo/KOBCLLM/cache"
)

tokenizer = AutoTokenizer.from_pretrained(
    "google/gemma-2-9b-it", 
    cache_dir="/workspace/youngwoo/KOBCLLM/cache"
)

def check_yes(response_content):
    # 모델을 사용하여 응답을 평가하는 로직을 구현합니다.
    # 현재는 단순히 "YES" 문자열을 확인하는 예시입니다.
    if "YES" in response_content.upper():
        return "YES"
    return "NO"

