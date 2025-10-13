import streamlit as st

# 이 파일은 멘토 전용 페이지입니다. 역할은 'mentor'로 고정됩니다.
ROLE = 'mentor'

# 페이지 상태 관리 (필요한 경우)
if 'page' not in st.session_state:
    st.session_state.page = 'signup_and_survey'
if 'survey_done' not in st.session_state:
    st.session_state.survey_done = False

# 사용자 친화적인 CSS (글씨를 최대한 크게)
st.markdown("""
<style>
    /* 전체 폰트 크기 및 색상 */
    .st-emotion-cache-183060u, .st-emotion-cache-1cyp687, .st-emotion-cache-16sx4w0, .st-emotion-cache-11r9c4z, .st-emotion-cache-19k721u {
        font-size: 1.4rem !important;
        color: #e0e0e0 !important;
    }
    
    /* 제목 */
    h1, h2, h3 {
        font-size: 2.5rem !important;
        color: #f7a300 !important;
        font-weight: bold;
    }
    h3 {
        font-size: 2rem !important;
    }
    
    /* 버튼 */
    .st-emotion-cache-19k721u, .st-emotion-cache-11r9c4z {
        font-size: 1.5rem !important;
        padding: 0.75rem 1.5rem;
    }
    
    /* 사이드바, 입력창, 버튼 배경색 */
    .st-emotion-cache-16sx4w0, .st-emotion-cache-q8s-b9p {
        background-color: #1e1e1e !important;
    }
    
    /* 라디오 버튼, 체크박스 폰트 */
    label.st-emotion-cache-p2w958 {
        font-size: 1.3rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 페이지 이동 함수
def set_page(page_name):
    st.session_state.page = page_name

# 사이드바 메뉴 (멘토 페이지에 맞게 재구성)
with st.sidebar:
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=50)
    st.title("멘토 전용 메뉴")
    st.markdown("---")
    if st.button("📝 회원가입/설문"): set_page('signup_and_survey')
    if st.button("👤 내 매칭"): set_page('my_matches')
    if st.button("🔎 멘티 찾기"): set_page('find_matches')
    if st.button("⚙️ 관리자 대시보드"): set_page('admin_dashboard')
    st.markdown("---")
    st.info("※ 데모용: 로컬에 저장됩니다.")


# --- 메인 페이지 로직 ---

if st.session_state.page == 'signup_and_survey':
    st.title("✨ 멘토 회원가입 및 설문")
    st.markdown("경험과 지혜를 나누어줄 **멘토님**을 모십니다.")
    
    # ----------------------------------------------------------------------
    # 1. 회원가입 폼
    # ----------------------------------------------------------------------
    with st.form("signup_form", clear_on_submit=False):
        st.subheader("1. 계정 정보")
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
                st.session_state.survey_done = True
    
    st.markdown("---")
    
    # ----------------------------------------------------------------------
    # 2. 설문조사 폼 (모든 항목 포함)
    # ----------------------------------------------------------------------
    if st.session_state.survey_done:
        st.header("2. 멘토 프로필 설문")
        st.write("성공적인 매칭을 위해 아래 항목에 답해주세요.")
        
        with st.form("survey_form", clear_on_submit=True):
            st.subheader("● 기본 정보")
            gender = st.radio("성별", ["남", "여", "기타"], horizontal=True)
            age_group = st.selectbox(
                "나이대",
                ["만 40세~49세", "만 50세~59세", "만 60세~69세", "만 70세~79세", "만 80세~89세", "만 90세 이상"]
            )

            # --- 직종 선택 (첨부된 이미지 기반) ---
            st.subheader("● 현재 직종")
            occupation = st.selectbox(
                "현재 직종",
                [
                    "경영자 (CEO, 사업주 등)", "행정관리", "의학/보건", "법률/행정", "교육", "연구개발/IT", 
                    "예술/디자인", "기술/기능", "서비스 전문", "일반 사무", "영업 원", "판매", "서비스", 
                    "의료/보건 서비스", "생산/제조", "건설/시설", "농림수산업", "운송/기계", "운송 관리", 
                    "청소/경비", "단순노무", "학생", "전업주부", "구직자/프리랜서(임시)", "기타 (직접 입력)"
                ]
            )

            # --- 가입 목적 및 대화 주제 ---
            st.subheader("● 가입 목적")
            purpose = st.multiselect(
                "멘토링을 통해 어떤 도움을 주고 싶으신가요? (복수선택 가능)",
                ["진로/커리어 조언", "학업/전문지식 조언", "사회/인생 경험 공유", "정서적 지지 및 대화"]
            )
            st.subheader("● 선호하는 대화 주제")
            topic = st.multiselect(
                "멘토링에서 주로 어떤 주제에 대해 이야기하고 싶으신가요?",
                ["진로·직업", "학업·전문 지식", "인생 경험·삶의 가치관", "대중문화·취미", "사회 문제·시사", "건강·웰빙"]
            )
            
            # --- 소통 스타일 ---
            st.subheader("● 선호하는 소통 방법")
            communication_method = st.radio("만남 방식", ["대면 만남", "화상 채팅", "일반 채팅"], horizontal=True)
            communication_day = st.multiselect("소통 가능한 요일 (복수선택)", ["월", "화", "수", "목", "금", "토", "일"])
            communication_time = st.multiselect("소통 가능한 시간대 (복수선택)", ["오전", "오후", "저녁", "밤"])
            
            st.subheader("● 소통 스타일")
            communication_style = st.radio(
                "평소 대화 시 본인과 비슷하다고 생각되는 것을 선택해주세요.",
                [
                    "연두부형: 조용하고 차분하게, 상대방 얘기를 경청하며 공감해 주는 편이에요.", 
                    "분위기메이커형: 활발하고 에너지가 넘쳐 대화를 이끌어가는 편이에요.",
                    "효율추구형: 주제를 체계적으로 정리하고 목표 지향적으로 대화하는 편이에요.",
                    "댐댐이형: 자유롭고 편안하게, 즉흥적으로 대화를 이어가는 편이에요.",
                    "감성 충만형: 감성적인 대화를 좋아하고 위로와 지지를 주는 편이에요.",
                    "냉철한 조언자형: 논리적이고 문제 해결 중심으로 조언을 주고받는 편이에요."
                ]
            )

            # --- 관심사 및 취향 ---
            st.subheader("● 관심사, 취향")
            hobby = st.multiselect(
                "1) 여가/취미 관련",
                ["독서", "음악 감상", "영화/드라마 감상", "게임 (PC/콘솔/모바일)", "운동/스포츠 관람", "미술·전시 감상", "여행", "요리/베이킹", "사진/영상 제작", "춤/노래"]
            )
            academic = st.multiselect(
                "2) 학문/지적 관심사",
                ["인문학 (철학, 역사, 문학 등)", "사회과학 (정치, 경제, 사회, 심리 등)", "자연과학 (물리, 화학, 생명과학 등)", "수학/논리 퍼즐", "IT/테크놀로지 (AI, 코딩, 로봇 등)", "환경/지속가능성"]
            )
            lifestyle = st.multiselect(
                "3) 라이프스타일",
                ["패션/뷰티", "건강/웰빙", "자기계발", "사회참여/봉사활동", "재테크/투자", "반려동물"]
            )
            pop_culture = st.multiselect(
                "4) 대중문화",
                ["K-POP", "아이돌/연예인", "유튜브/스트리밍", "웹툰/웹소설", "스포츠 스타"]
            )

            # --- 추구하는 성향 (새로움 vs 안정감 포함) ---
            st.subheader("● 5) 특별한 취향/성향")
            
            # 새로운 경험 vs 안정감은 별도의 라디오 버튼으로 분리
            new_vs_stable = st.radio(
                "새로운 경험과 안정감 중 어느 것을 더 선호하시나요?",
                ["새로운 경험을 추구합니다", "안정적이고 익숙한 것을 선호합니다"]
            )
            
            # 나머지 성향은 체크박스로
            preference = st.multiselect(
                "본인에게 해당하는 성향을 모두 선택해주세요.",
                ["혼자 보내는 시간 선호", "친구들과 어울리기 선호", "실내 활동 선호", "야외 활동 선호"]
            )

            survey_submitted = st.form_submit_button("설문 완료하고 매칭 시작하기")
            if survey_submitted:
                st.balloons()
                st.success("🎉 멘토 프로필 설문이 완료되었습니다! 이제 멘티를 찾을 수 있습니다.")
                set_page('find_matches')
        
        st.markdown("---")
        st.info("✅ 모든 설문 항목을 작성하고 **'설문 완료하고 매칭 시작하기'** 버튼을 눌러주세요.")

elif st.session_state.page == 'find_matches':
    st.title("🔎 멘티 찾기")
    st.write("멘토님에게 적합한 멘티들을 추천합니다.")
    st.info("✅ 아래 목록에서 마음에 드는 멘티를 선택해주세요.")
    # 가상 데이터
    st.info("김철수 (멘티), 박영희 (멘티)") 

elif st.session_state.page == 'my_matches':
    st.title("👤 내 매칭")
    st.write("현재 매칭된 멘티와의 소통 공간입니다.")
    st.info("✅ 아직 매칭된 상대가 없습니다. '멘티 찾기'를 통해 상대를 찾아보세요.")

elif st.session_state.page == 'admin_dashboard':
    st.title("⚙️ 관리자 대시보드")
    st.write("플랫폼 전체 회원 현황 및 매칭 현황을 관리합니다.")
    st.warning("✅ 이 페이지는 관리자만 접근할 수 있습니다.")
