import requests

# FastAPI 서버 URL 설정 (포트와 주소는 필요에 따라 조정)
url = "http://127.0.0.1:8000/posts"

# 등록할 게시물 데이터 설정
post_data = {
    "title": "테스트 제목",
    "content": "테스트 내용",
    "author": "작성자 이름"
}

# POST 요청을 보내고 응답 받기
response = requests.post(url, json=post_data)

# 응답 출력
if response.status_code == 200:
    print("게시물 등록 성공:", response.json())
else:
    print("게시물 등록 실패:", response.status_code, response.text)
