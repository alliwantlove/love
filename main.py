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
        return JSONResponse(content={
            "version": "2.0",
            "template": {
                "outputs": [{"simpleText": {"text": "이 API는 POST 방식으로 사용해야 합니다."}}]
            }
        })

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

@app.post("/location")
async def location_handler(request: Request):
    body = await request.json()
    location = body.get("userRequest", {}).get("location", {})

    name = location.get("name", "위치 정보 없음")
    lat = location.get("lat")
    lng = location.get("lng")

    if lat and lng:
        prompt = f"위도 {lat}, 경도 {lng} 근처에 갈 만한 명소를 추천해줘. 장소명과 설명도 함께."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
    else:
        answer = f"위치 정보가 부족합니다. name: {name}, 위도: {lat}, 경도: {lng}"

    return JSONResponse(content={
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": answer}}]
        }
    })
