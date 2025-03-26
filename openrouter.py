from openai import OpenAI
API_KEY = "sk-fa0200cf1b9d4d4980aad2e883db4807"

# DeepSeek API 키와 기본 URL로 클라이언트 초기화
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1")

# deepseek-chat 모델을 사용하여 비스트리밍 채팅 완료 요청 생성
response = client.chat.completions.create(
	model="deepseek-chat",
    messages=[
    	{"role": "system", "content": "You are a useful assistant"},
        {"role": "user", "content": "DeepSeek API가 어떻게 작동하는지 설명해 줄 수 있나요?"} 
	],
    stream=False  # 스트리밍 응답을 위해 True로 설정
) 

# 응답 내용 출력
print(response.choices[0].message.content)