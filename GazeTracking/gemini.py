import google.generativeai as genai #gemini Testing code

API_KEY = "AIzaSyBSuHxEGpxivX39ZPjy_cuI1jvDq5MkdyM"  #테스트 키

genai.configure(api_key=API_KEY)

try:
    # 모델 정의 및 콘텐츠 생성
    model = genai.GenerativeModel('gemini-2.5-flash') 
    question = input("질문 : ")
    response = model.generate_content(question)
    print("응답:", response.text)
    
except Exception as e:
    # 키가 유효하지 않거나 API 호출 중 다른 오류가 발생한 경우 처리
    print(f"API 호출 중 오류 발생: 키가 올바른지 확인하세요. 오류 내용: {e}")