import streamlit as st

from dotenv import load_dotenv
from llm import get_ai_response

st.set_page_config(page_title="국민연금법 챗봇", page_icon='🤖')

st.title("🤖 국민연금법 챗봇")
st.caption("국민연금법 관련된 모든것을 답해드립니다!")

load_dotenv()
 
# Session State 통해서 이전 메세지를 저장
if 'message_list' not in st.session_state:
    st.session_state.message_list = []

# print(f"before == {st.session_state.message_list}")

# 반복문 통해서 사용자 과거에 입력했던 메세지 표시
for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])



# 입력창
if user_question := st.chat_input(placeholder="국민연금법 관련된 궁금한 내용들을 말씀해주세요!"):
    # 사용자 최근에 입력하는 메세지 표시
    with st.chat_message("user"):
        st.write(user_question)
    # session_state를 담는다.
    st.session_state.message_list.append({"role": "user", "content":user_question})

    with st.spinner("답변 생성 중"):
        ai_response = get_ai_response(user_question)

    with st.chat_message("ai"):
        ai_message = st.write_stream(ai_response)
    # session_state를 담는다.
    st.session_state.message_list.append({"role": "ai", "content":ai_message})


# print(f"after == {st.session_state.message_list}")