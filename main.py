from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/location")
async def location_handler(request: Request):
    body = await request.json()
    location = body.get("userRequest", {}).get("location", {})

    name = location.get("name", "위치 정보 없음")
    lat = location.get("lat")
    lng = location.get("lng")

    return JSONResponse(content={
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": f"위치: {name}\n좌표: {lat}, {lng}"
                }
            }]
        }
    })