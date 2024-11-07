import streamlit as st
import openai

# 제목과 설명 표시
st.title("🌍 여행 챗봇")
st.write(
    "여행 챗봇에 오신 것을 환영합니다! 이 챗봇은 다양한 여행지에 대한 추천, 일정, 음식 정보를 제공합니다. "
    "아래에 OpenAI API 키를 입력하고 여행지, 명소, 음식 등과 관련된 질문을 해보세요."
)

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API 키", type="password")
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    openai.api_key = openai_api_key

    # 세션 상태에 메시지 저장 설정
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력에 맞춰 프롬프트 생성 함수
    def generate_prompt(user_input):
        if "일정" in user_input or "계획" in user_input:
            return f"{user_input}에 대한 여행 일정을 작성해 주세요."
        elif "음식" in user_input or "식당" in user_input:
            return f"{user_input}의 인기 음식과 식당을 추천해 주세요."
        elif "명소" in user_input or "볼거리" in user_input:
            return f"{user_input}의 주요 명소와 할 일 목록을 알려주세요."
        else:
            return f"이 여행 관련 질문에 답변해 주세요: {user_input}"

    # 사용자 입력 필드
    if prompt := st.chat_input("여행 계획에 대해 질문해 보세요!"):
        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 사용자 의도에 따른 프롬프트 생성
        refined_prompt = generate_prompt(prompt)
        try:
            # OpenAI API 호출 및 응답 생성
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful travel assistant."},
                    {"role": "user", "content": refined_prompt}
                ]
            )

            # Assistant 응답 저장 및 표시
            assistant_reply = response.choices[0].message["content"]
            with st.chat_message("assistant"):
                st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
