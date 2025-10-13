import streamlit as st
import pandas as pd
import uuid # 고유 ID 생성을 위해 import

# 이 파일은 멘토 전용 페이지입니다. 역할은 'mentor'로 고정됩니다.
ROLE = 'mentor'

# 페이지 상태 관리
if 'page' not in st.session_state:
    st.session_state.page = 'signup_and_survey'
if 'survey_done' not in st.session_state:
    st.session_state.survey_done = False
# 🚨🚨🚨 실제 데이터 저장소 (세션이 유지되는 동안 데이터 보존) 🚨🚨🚨
if 'mentor_data' not in st.session_state:
    st.session_state.mentor_data = []


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
    
    /* 정보 표시 영역 (info, success 등) */
    .stAlert {
        font-size: 1.3rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 페이지 이동 함수
def set_page(page_name):
    st.session_state.page = page_name

# 사이드바 메뉴 (관리자 대시보드가 맨 마지막)
with st.sidebar:
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=50)
    st.title("멘토 전용 메뉴")
    st.markdown("---")
    if st.button("📝 회원가입/설문"): set_page('signup_and_survey')
    if st.button("👤 내 매칭"): set_page('my_matches')
    if st.button("🔎 멘티 찾기"): set_page('find_matches')
    st.markdown("---")
    if st.button("⚙️ 관리자 대시보드"): set_page('admin_dashboard')
    st.markdown("---")
    st.info("※ 데모용: 로컬에 저장됩니다.")


# ----------------------------------------------------------------------
# 관리자 대시보드 페이지 함수 (실제 회원 데이터 조회)
# ----------------------------------------------------------------------
def admin_dashboard():
    st.title("⚙️ 관리자 대시보드")
    st.write("플랫폼 전체 회원 현황 및 매칭 성과를 관리합니다.")
    st.error("🚨 **주의**: 이 페이지는 플랫폼의 **핵심 데이터**를 다루므로, 운영진만 접근해야 합니다.")
    st.warning("⚠️ **중요**: 이 데이터는 **현재 Streamlit 세션에만 임시로 저장**되며, 앱을 재실행하면 사라집니다.")
    
    st.markdown("---")
    
    # 멘토 데이터 로드
    mentors = st.session_state.mentor_data
    
    st.subheader(f"👥 멘토 회원 목록 (총 {len(mentors)}명)")
    
    if not mentors:
        st.info("아직 가입된 멘토 회원이 없습니다. 회원가입 페이지에서 테스트로 등록해주세요.")
        return

    # DataFrame 생성
    df_mentors = pd.DataFrame(mentors)
    
    # 표시할 컬럼 순서 지정 (필요 없는 세부 설문 항목은 숨김)
    display_columns = ['ID', '이름', '이메일', '가입일', '나이대', '성별', '현재 직종', '만남 방식', '소통 스타일', '매칭 상태']
    df_display = df_mentors[display_columns]

    # --------------------------------
    # 필터링/검색 UI
    # --------------------------------
    st.markdown("#### 🔍 멘토 검색 및 필터링")
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        search_term = st.text_input("이름, 이메일, 직종으로 검색")
    
    with col_filter2:
        selected_status = st.selectbox("매칭 상태별 필터", ['전체', '매칭 중', '매칭 대기'])

    # 데이터 필터링 로직
    df_filtered = df_display
    
    if search_term:
        df_filtered = df_filtered[
            df_filtered['이름'].str.contains(search_term, case=False, na=False) |
            df_filtered['이메일'].str.contains(search_term, case=False, na=False) |
            df_filtered['현재 직종'].str.contains(search_term, case=False, na=False)
        ]
        
    if selected_status != '전체':
        df_filtered = df_filtered[df_filtered['매칭 상태'] == selected_status]

    
    # --------------------------------
    # 필터링 결과 표시 및 관리 기능
    # --------------------------------
    st.markdown(f"**총 {len(df_filtered)}건**의 멘토 회원 정보가 표시됩니다.")
    
    # 멘토 목록 테이블 표시
    st.dataframe(df_filtered, use_container_width=True)

    st.markdown("---")

    st.subheader("🛠️ 멘토 관리 기능")
    st.info("여기에 선택된 멘토에 대한 강제 매칭, 정지, 프로필 수정 등의 기능이 구현됩니다.")
    
    col_admin1, col_admin2, col_admin3 = st.columns(3)
    with col_admin1:
        if st.button("회원 상세 프로필 보기"):
            st.warning("⚠️ 특정 멘토의 상세 프로필을 열람하는 기능이 실행됩니다.")
    with col_admin2:
        if st.button("선택된 멘토 강제 정지"):
            st.error("❌ 멘토 정지 기능이 실행되었습니다.")
    with col_admin3:
        if st.button("선택된 멘토에게 개별 알림"):
            st.success("✅ 개별 알림 발송 기능이 실행되었습니다.")


# --- 메인 페이지 로직 ---

if st.session_state.page == 'signup_and_survey':
    st.title("✨ 멘토 회원가입 및 설문")
    st.markdown("경험과 지혜를 나누어줄 **멘토님**을 모십니다.")
    
    # ----------------------------------------------------------------------
    # 1. 회원가입 폼
    # ----------------------------------------------------------------------
    with st.form("signup_form", clear_on_submit=False):
        st.subheader("1. 계정 정보 입력")
        
        # 폼 내부 변수 (설문폼과 공유하기 위해 폼 바깥에 선언)
        name_input = st.text_input("이름", key='signup_name')
        email_input = st.text_input("이메일 (로그인 ID)", key='signup_email')
        password_input = st.text_input("비밀번호", type="password", key='signup_password')
        confirm_password_input = st.text_input("비밀번호 확인", type="password", key='signup_confirm_password')
        
        submitted = st.form_submit_button("회원가입하고 설문하기")
        if submitted:
            if not name_input or not email_input or not password_input:
                st.error("❌ 모든 계정 정보를 입력해주세요.")
            elif password_input != confirm_password_input:
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

            # --- 직종 선택 ---
            st.subheader("● 현재 직종")
            occupation_options = [
                "경영자 (CEO, 사업주 등)", "행정관리", "의학/보건", "법률/행정", "교육", "연구개발/IT", 
                "예술/디자인", "기술/기능", "서비스 전문", "일반 사무", "영업원", "판매", "서비스", 
                "의료/보건 서비스", "생산/제조", "건설/시설", "농림수산업", "운송/기계", "운송 관리", 
                "청소/경비", "단순노무", "전업주부", "구직자/프리랜서(임시)", "기타 (직접 입력)"
            ]
            occupation = st.selectbox("현재 직종", occupation_options)

            # --- 가입 목적 및 대화 주제 ---
            st.subheader("● 멘토링 목적 및 주제")
            purpose = st.multiselect(
                "멘토링을 통해 어떤 도움을 주고 싶으신가요? (복수선택 가능)",
                ["진로/커리어 조언", "학업/전문지식 조언", "사회/인생 경험 공유", "정서적 지지 및 대화"]
            )
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
            communication_style = st.selectbox(
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

            # --- 추구하는 성향 ---
            st.subheader("● 5) 특별한 취향/성향")
            
            new_vs_stable = st.radio(
                "새로운 경험과 안정감 중 어느 것을 더 선호하시나요?",
                ["새로운 경험을 추구합니다", "안정적이고 익숙한 것을 선호합니다"]
            )
            
            preference = st.multiselect(
                "본인에게 해당하는 성향을 모두 선택해주세요.",
                ["혼자 보내는 시간 선호", "친구들과 어울리기 선호", "실내 활동 선호", "야외 활동 선호"]
            )

            survey_submitted = st.form_submit_button("설문 완료하고 매칭 시작하기")
            if survey_submitted:
                
                # 멘토 데이터 수집 및 저장
                mentor_profile = {
                    'ID': str(uuid.uuid4())[:8], # 고유 ID 생성
                    '이름': st.session_state.signup_name,
                    '이메일': st.session_state.signup_email,
                    '가입일': pd.Timestamp.now().strftime("%Y-%m-%d"),
                    '매칭 상태': '매칭 대기',
                    
                    '성별': gender,
                    '나이대': age_group,
                    '현재 직종': occupation,
                    '멘토링 목적': purpose,
                    '주요 주제': topic,
                    '만남 방식': communication_method,
                    '가능 요일': communication_day,
                    '가능 시간': communication_time,
                    '소통 스타일': communication_style,
                    '취미': hobby,
                    '학문': academic,
                    '라이프스타일': lifestyle,
                    '대중문화': pop_culture,
                    '경험 선호': new_vs_stable,
                    '선호 성향': preference
                }
                
                # 🚨 세션 상태에 데이터 추가 (실제 DB 역할)
                st.session_state.mentor_data.append(mentor_profile)
                
                # 설문 완료 후 상태 초기화 및 페이지 이동
                st.session_state.survey_done = False
                st.session_state.signup_name = ''
                st.session_state.signup_email = ''
                st.session_state.signup_password = ''
                st.session_state.signup_confirm_password = ''
                
                st.balloons()
                st.success("🎉 멘토 프로필 설문이 완료되었습니다! 이제 멘티를 찾을 수 있습니다.")
                set_page('find_matches')
        
        st.markdown("---")
        st.info("✅ 모든 설문 항목을 작성하고 **'설문 완료하고 매칭 시작하기'** 버튼을 눌러주세요.")

elif st.session_state.page == 'find_matches':
    st.title("🔎 멘티 찾기")
    st.write("멘토님에게 적합한 멘티들을 추천합니다.")
    st.info("✅ 현재 매칭 가능한 멘티가 없습니다. 곧 새로운 멘티가 가입될 예정입니다.") 

elif st.session_state.page == 'my_matches':
    st.title("👤 내 매칭")
    st.write("현재 매칭된 멘티와의 소통 공간입니다.")
    st.info("✅ 아직 매칭된 상대가 없습니다. '멘티 찾기'를 통해 상대를 찾아보세요.")

elif st.session_state.page == 'admin_dashboard':
    admin_dashboard()
