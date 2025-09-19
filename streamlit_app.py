import streamlit as st

# 페이지 상태 관리
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'signup_done' not in st.session_state:
    st.session_state.signup_done = False

# 사용자 친화적인 CSS (큰 폰트, 고대비)
st.markdown("""
<style>
    .st-emotion-cache-183060u, .st-emotion-cache-1cyp687, .st-emotion-cache-16sx4w0, .st-emotion-cache-11r9c4z, .st-emotion-cache-19k721u {
        font-size: 1.25rem !important; /* 전체 폰트 크기 증가 */
    }
    .st-emotion-cache-19k721u, .st-emotion-cache-11r9c4z { /* stButton, etc */
        font-size: 1.35rem !important;
    }
    .st-emotion-cache-16sx4w0 {
        background-color: #1e1e1e !important;
        color: #e0e0e0 !important;
    }
    .st-emotion-cache-q8s-b9p {
        background-color: #1e1e1e !important;
        color: #e0e0e0 !important;
    }
    h1, h2, h3 {
        color: #f7a300;
        font-weight: bold;
    }
    body {
        background-color: #121212 !important;
    }
</style>
""", unsafe_allow_html=True)

# 페이지 이동 함수
def set_page(page_name):
    st.session_state.page = page_name

# 사이드바 메뉴
with st.sidebar:
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=50)
    st.title("메뉴")
    st.markdown("---")
    if st.button("🏠 홈"): set_page('home')
    if st.button("📝 회원가입"): set_page('signup')
    if st.button("👤 내 매칭"): set_page('my_matches')
    if st.button("🔎 매칭 찾기"): set_page('find_matches')
    if st.button("⚙️ 관리자 대시보드"): set_page('admin_dashboard')
    st.markdown("---")
    st.info("※ 데모용: 로컬에 저장됩니다.")

# --- 메인 페이지 로직 ---

if st.session_state.page == 'home':
    st.title("👴👵 노인 멘토 - 🧑‍🎓 청년 멘티 매칭 플랫폼")
    st.markdown("가입 설문을 바탕으로 맞춤형 멘토-멘티를 추천합니다.")
    st.write("함께 성장하는 지혜로운 만남, 지금 시작하세요!")
    if st.button("회원가입하고 시작하기"):
        set_page('signup')

elif st.session_state.page == 'signup':
    st.title("회원가입 및 설문")
    
    # 회원가입 폼
    with st.form("signup_form", clear_on_submit=False):
        st.subheader("계정 정보")
        role = st.selectbox("멘토/멘티 중 어떤 역할을 맡고 싶으신가요?", ["멘티", "멘토"])
        name = st.text_input("이름")
        email = st.text_input("이메일 (로그인 ID)")
        password = st.text_input("비밀번호", type="password")
        confirm_password = st.text_input("비밀번호 확인", type="password")
        
        submitted = st.form_submit_button("회원가입하고 설문하기")
        if submitted:
            if password != confirm_password:
                st.error("❌ 비밀번호가 일치하지 않습니다. 다시 확인해주세요.")
            else:
                st.success("✅ 회원가입 정보가 확인되었습니다! 아래 설문을 계속 진행해주세요.")
                st.session_state.signup_done = True
                
    # 설문조사 폼
    if st.session_state.signup_done:
        st.markdown("---")
        st.header("프로필 설문")
        st.write("성공적인 매칭을 위해 아래 항목에 답해주세요.")

        with st.form("survey_form", clear_on_submit=True):
            st.subheader("● 개인 정보")
            gender = st.radio("성별", ["남", "여", "기타"], horizontal=True)
            age_group = st.selectbox(
                "나이대",
                ["만 13세~19세", "만 20세~29세", "만 30세~39세", "만 40세~49세", "만 50세~59세", "만 60세~69세", "만 70세~79세", "만 80세~89세", "만 90세 이상"]
            )
            occupation = st.selectbox(
                "현재 직종",
                [
                    "학생", "전업주부", "구직자", "경영자", "행정관리", "의학/보건", "법률/행정", "교육", "연구개발/IT", "예술/디자인",
                    "기술/기능", "서비스 전문", "운송/기계", "운송 관리", "청소/경비", "단순노무", "일반 사무", "영업 원", "판매",
                    "서비스", "의료/보건 서비스", "생산/제조", "건설/시설", "농림수산업", "기타 (직접 입력)"
                ]
            )
            if occupation == "기타 (직접 입력)":
                other_occupation = st.text_input("직접 직종을 입력해주세요")
            
            st.subheader("● 소통 스타일")
            communication_style = st.radio("선호하는 소통 방법", ["대면 만남", "화상 채팅", "일반 채팅"], horizontal=True)
            communication_time = st.multiselect("소통 가능한 시간대 (복수선택)", ["오전", "오후", "저녁", "밤"])
            
            st.subheader("● 본인이 추구하는 성향")
            new_vs_stable = st.selectbox(
                "새로움과 안정감 중 어느 쪽을 더 추구하시나요?",
                ["새로운 경험을 추구합니다", "안정적이고 익숙한 것을 선호합니다"]
            )
            
            # --- 기타 설문 항목 ---
            st.subheader("● 가입 목적")
            purpose = st.multiselect(
                "멘토링을 통해 얻고 싶은 것은 무엇인가요? (복수선택 가능)",
                ["진로 / 커리어 조언", "학업 / 전문지식 공유", "사회, 인생 경험 공유", "정서적 지지와 대화"]
            )

            st.subheader("● 선호하는 대화 주제")
            topic = st.multiselect(
                "멘토링에서 주로 어떤 주제에 대해 이야기하고 싶으신가요?",
                ["진로·직업", "학업·전문 지식", "인생 경험·삶의 가치관", "대중문화·취미", "사회 문제·시사", "건강·웰빙"]
            )
            
            st.subheader("● 관심사, 취향")
            st.write("1) 여가/취미 관련")
            hobby = st.multiselect(
                "관심 있는 취미를 모두 선택해주세요.",
                ["독서", "음악 감상", "영화/드라마 감상", "게임", "운동/스포츠 관람", "미술·전시 감상", "여행", "요리/베이킹", "사진/영상 제작", "춤/노래"]
            )

            st.write("2) 학문/지적 관심사")
            academic = st.multiselect(
                "관심 있는 학문 분야를 모두 선택해주세요.",
                ["인문학", "사회과학", "자연과학", "수학/논리 퍼즐", "IT/테크놀로지", "환경/지속가능성"]
            )
            
            st.write("3) 라이프스타일")
            lifestyle = st.multiselect(
                "선호하는 라이프스타일을 모두 선택해주세요.",
                ["패션/뷰티", "건강/웰빙", "자기계발", "사회참여/봉사활동", "재테크/투자", "반려동물"]
            )

            st.write("4) 대중문화")
            pop_culture = st.multiselect(
                "관심 있는 대중문화를 모두 선택해주세요.",
                ["K-POP", "아이돌/연예인", "유튜브/스트리밍", "웹툰/웹소설", "스포츠 스타"]
            )
            
            survey_submitted = st.form_submit_button("설문 완료하고 매칭 시작하기")
            if survey_submitted:
                st.balloons()
                st.success("🎉 설문조사가 완료되었습니다! 이제 맞춤형 멘토/멘티를 찾을 수 있습니다.")
                st.json({
                    "목적": purpose, "주제": topic, "성향": new_vs_stable, "취미": hobby,
                    "학문": academic, "라이프스타일": lifestyle, "대중문화": pop_culture
                })
                set_page('find_matches')

elif st.session_state.page == 'find_matches':
    st.title("🔎 매칭 찾기")
    st.write("나에게 맞는 멘토/멘티를 찾아보세요.")
    # 여기에 매칭 결과 표시 로직 추가

elif st.session_state.page == 'my_matches':
    st.title("👤 내 매칭")
    st.write("현재 매칭된 멘토/멘티와의 소통 공간입니다.")
    # 여기에 매칭된 상대방 정보 및 채팅 기능 추가

elif st.session_state.page == 'admin_dashboard':
    st.title("⚙️ 관리자 대시보드")
    st.write("플랫폼 전체 회원 현황 및 매칭 현황을 관리합니다.")
    # 여기에 관리자용 기능 추가
