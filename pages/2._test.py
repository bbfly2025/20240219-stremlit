import streamlit as st
import pandas as pd
from datetime import datetime


st.title('자유게시판 💬')
# 파일 경로 설정
DATA_FILE = 'posts.csv'

# 삭제 비밀번호 설정
DELETE_PASSWORD = "2025"

# 세션 상태 초기화
if 'delete_index' not in st.session_state:
    st.session_state.delete_index = -1

# 게시글 불러오기 또는 초기화
try:
    posts = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    posts = pd.DataFrame(columns=['Date', 'Post'])
    posts.to_csv(DATA_FILE, index=False)

# 사용자 입력 받기
user_input = st.text_area("글 작성하기", "여기에 글을 작성하세요.")

# '글 작성' 버튼 처리
if st.button('글 올리기'):
    if user_input and not user_input.isspace():
        new_post = pd.DataFrame({'Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')], 'Post': [user_input]})
        posts = pd.concat([posts, new_post], ignore_index=True)
        posts.to_csv(DATA_FILE, index=False)
        st.success('글이 성공적으로 작성되었습니다!')

# 게시글과 삭제 버튼 표시 및 비밀번호 입력 처리
for index, row in posts.iterrows():
    st.write(f"{row['Date']} - {row['Post']}", key=f"post_{index}")
    delete_button = st.button('X', key=f"delete_{index}")
    
    if delete_button:
        st.session_state.delete_index = index  # 삭제할 게시글 인덱스 업데이트

# 선택된 게시글이 있고, 비밀번호 입력 처리
if st.session_state.delete_index != -1:
    pwd_input = st.text_input("비밀번호를 입력하세요", type="password")
    if pwd_input:
        if pwd_input == DELETE_PASSWORD:
            # 올바른 비밀번호 입력 시 게시글 삭제
            posts = posts.drop(st.session_state.delete_index).reset_index(drop=True)
            posts.to_csv(DATA_FILE, index=False)
            st.success('글이 삭제되었습니다.')
            st.session_state.delete_index = -1  # 삭제 인덱스 초기화
            st.experimental_rerun()
        else:
            st.error('비밀번호가 잘못되었습니다.')

# 게시글 표시
st.write("모든 게시글:")
st.dataframe(posts)
