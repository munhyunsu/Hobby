import os
from google import genai

# 1. python-dotenv 패키지가 있다면 .env 로드
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 2. 환경 변수에서 API 키 가져오기
API_KEY = os.getenv("GEMINI_API_KEY")

# 3. 만약 dotenv 패키지가 없거나 환경 변수가 없으면 .env 파일 직접 파싱 (보조 방식)
if not API_KEY and os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

# API 키 유효성 체크
if not API_KEY or API_KEY == "YOUR_ACTUAL_API_KEY_HERE":
    raise ValueError("❌ .env 파일에 올바른 GEMINI_API_KEY를 입력해 주세요.")

try:
    # 클라이언트 초기화
    client = genai.Client(api_key=API_KEY)

    # [1/2] 기본 API 키 연결 확인 (텍스트 모델)
    print("🔄 [1/2] API 키 연결 확인 중...")
    text_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="API 키 테스트입니다. '정상 동작 중'이라고 답변해 주세요.",
    )
    print(f"✅ API 연결 성공! 응답: {text_response.text.strip()}\n")

    # [2/2] Nano Banana 이미지 생성 테스트
    print("🎨 [2/2] Nano Banana 이미지 생성 테스트 중...")
    image_response = client.models.generate_content(
        model="gemini-3.1-flash-image",
        contents="A cute yellow banana character wearing sunglasses, digital art style",
    )

    # 생성된 이미지 저장
    saved = False
    for part in image_response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save("test_banana.png")
            print("🎉 Nano Banana 동작 완료! 'test_banana.png' 파일로 저장되었습니다.")
            saved = True
            break

    if not saved and image_response.text:
        print(f"ℹ️ 모델 응답: {image_response.text}")

except Exception as e:
    print("\n❌ 테스트 실패!")
    print(f"오류 메시지: {e}")

