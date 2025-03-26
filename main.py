from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.api_route("/recommend", methods=["GET", "POST"])
async def recommend(request: Request):
    try:
        body = await request.json()
        utterance = body.get("userRequest", {}).get("utterance", "")
    except:
        # GET 요청 테스트일 경우, 임시 메시지
        return JSONResponse(content={
            "version": "2.0",
            "template": {
                "outputs": [{"simpleText": {"text": "이 API는 POST 방식으로 사용해야 합니다."}}]
            }
        })

    # GPT 호출
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{utterance}에 어울리는 장소 추천해줘"}
        ]
    )

    answer = response.choices[0].message.content.strip()

    return JSONResponse(content={
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": answer}}]
        }
    })