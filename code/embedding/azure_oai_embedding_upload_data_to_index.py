##################################################
# Azure AI Search에 미리 만들어 놓은 인덱스에 Azure OpenAI 모델로 임베딩 시킨 데이터를 업로드하는 모듈
##################################################

import os
from openai import AzureOpenAI

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

os.system('cls' if os.name == 'nt' else 'clear')

# 필수 환경변수 획득
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_EMBEDDING_DEPLOYNAME = os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYNAME')
AZURE_OPENAI_EMBEDDING_LARGE_DEPLOYNAME = os.getenv('AZURE_OPENAI_EMBEDDING_LARGE_DEPLOYNAME')
AZURE_VECTOR_SEARCH_ENDPOINT = os.getenv('AZURE_VECTOR_SEARCH_ENDPOINT')
AZURE_VECTOR_SEARCH_API_KEY = os.getenv('AZURE_VECTOR_SEARCH_API_KEY')
AZURE_VECTOR_SEARCH_INDEXNAME = os.getenv('AZURE_VECTOR_SEARCH_INDEXNAME')


client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-12-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)
 
with open('C:\\Users\\KTDS\\Documents\\git_repos\\nlweb_poc\\data\\json\\scifi_movies_schemas - 복사본.txt', 'rb') as f:
    fr_ = f.read()
    #print( fr_ )

response = client.embeddings.create(
    input=fr_,
    model=AZURE_OPENAI_EMBEDDING_DEPLOYNAME
)

embedding_vector = response.data[0].embedding
#print( embedding_vector )


# Azure AI Search에 미리 만들어 놓은 인덱스에 Azure OpenAI 모델로 임베딩 시킨 데이터 업로드
import requests

url = f"{AZURE_VECTOR_SEARCH_ENDPOINT}/indexes/{AZURE_VECTOR_SEARCH_INDEXNAME}/docs/index?api-version=2023-10-01-Preview"
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_VECTOR_SEARCH_API_KEY
}
data = {
    "value": [
        {
            "@search.action": "upload",
            "id": "1",
            "name": "텍스트 데이터",
            "embedding": embedding_vector
        }
    ]
}

resp = requests.post(url, headers=headers, json=data)
#print( resp )
print( resp.status_code )
print( resp.reason )
print( resp.text )  # 에러 상세 메시지 출력
