from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import openai
import os

app = FastAPI()

# OpenAI 키 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")  # 또는 직접 문자열로 대입해도 OK

@app.post("/recommend")
async def recommend(request: Request):
    body = await request.json()
    user_input = body.get("userRequest", {}).get("utterance", "")

    # ChatGPT 요청
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{user_input} 에 어울리는 장소 추천해줘"}]
    )

    answer = response.choices[0].message.content.strip()

    # 카카오 오픈빌더 응답 포맷으로 구성
    kakao_response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }

    return JSONResponse(content=kakao_response)