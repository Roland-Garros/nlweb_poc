##################################################
# Azure AI Search에 미리 만들어 놓은 인덱스에 Azure OpenAI 모델로 임베딩 시킨 데이터를 업로드하는 모듈
##################################################

import os
import requests
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

url = f"{AZURE_VECTOR_SEARCH_ENDPOINT}/indexes/{AZURE_VECTOR_SEARCH_INDEXNAME}/docs/index?api-version=2023-10-01-Preview"
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_VECTOR_SEARCH_API_KEY
}

schema_json = """
{
  "type": "object",
  "properties": {
    "@type": { "type": "string" },
    "@id": { "type": "string" },
    "name": { "type": "string" },
    "datePublished": { "type": ["integer", "string"] },
    "director": {
      "type": "object",
      "properties": {
        "@type": { "type": "string" },
        "name": { "type": "string" },
        "@id": { "type": "string" }
      },
      "required": ["@type", "name", "@id"]
    },
    "aggregateRating": {
      "type": "object",
      "properties": {
        "@type": { "type": "string" },
        "ratingValue": { "type": ["number", "string"] }
      },
      "required": ["@type", "ratingValue"]
    },
    "image": { "type": "string" },
    "inLanguage": { "type": "string" },
    "url": { "type": "string" },
    "description": { "type": "string" },
    "actor": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "@type": { "type": "string" },
          "@id": { "type": "string" },
          "name": { "type": "string" },
          "characterName": { "type": "string" }
        },
        "required": ["@type", "@id", "name"]
      }
    }
  },
  "required": ["@type", "@id", "name", "datePublished", "director", "aggregateRating", "image", "inLanguage", "url", "description", "actor"]
}
"""
 
with open('C:\\Users\\KTDS\\Documents\\git_repos\\nlweb_poc\\data\\json\\scifi_movies_schemas_1_4.txt', 'rb') as f:
    fr = f.readlines()
    #print( fr_ )
    for i,line in enumerate(fr):
        line = line.decode('utf-8').strip()
        #print(line)
        if line:
            l_ = line.split('\t')[1]
            #print( l_ )
            d_ = eval(l_)
            #print( type(d_) )
            #print( d_ )
            print('='*50)
            print( f'id: {str(i+1)}' )
            print( f'url: {d_.get("url")}' )
            print( f'name: {d_.get("name")}' )
            print( f'site: {d_.get("url")}' )
            print( f'description: {d_.get("description")}' )
            # Azure AI Search에 미리 만들어 놓은 인덱스에 Azure OpenAI 모델로 임베딩 시킨 데이터 업로드
            data = {
                "value": [
                    {
                        "@search.action": "upload",
                        "id": str(i+1),
                        "url": d_.get("url"),
                        "name": d_.get("name"),
                        "site": d_.get("url"),
                        "description": d_.get("description"),
                        "schema_json": schema_json,
                        "embedding": client.embeddings.create(
                            input=l_,
                            model=AZURE_OPENAI_EMBEDDING_DEPLOYNAME
                        ).data[0].embedding
                    }
                ]
            }
            resp = requests.post(url, headers=headers, json=data)
            print( resp.status_code )
            print( resp.reason )
            print( resp.text )

"""
response = client.embeddings.create(
    input=fr_,
    model=AZURE_OPENAI_EMBEDDING_DEPLOYNAME
)

embedding_vector = response.data[0].embedding
#print( embedding_vector )


# Azure AI Search에 미리 만들어 놓은 인덱스에 Azure OpenAI 모델로 임베딩 시킨 데이터 업로드
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
"""