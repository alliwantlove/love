from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📍 위치 기반 추천 처리용
@app.post("/location")
async def location_handler(request: Request):
    body = await request.json()
    location = body.get("userRequest", {}).get("location", {})

    name = location.get("name", "위치 정보 없음")
    lat = location.get("lat", "알 수 없음")
    lng = location.get("lng", "알 수 없음")

    return JSONResponse(content={
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": f"📍 위치: {name}\n위도: {lat}\n경도: {lng}"
                }
            }]
        }
    })

# 💬 일반 텍스트 추천 처리용
@app.api_route("/recommend", methods=["GET", "POST"])
async def recommend(request: Request):
    try:
        body = await request.json()
        utterance = body.get("userRequest", {}).get("utterance", "")
    except:
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
