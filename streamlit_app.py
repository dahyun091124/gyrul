import streamlit as st
import pandas as pd
import uuid
import datetime
import os 

# 이 파일은 멘토 전용 페이지입니다.
ROLE = 'mentor'

# 🚨 관리자 대시보드 비밀번호 설정 🚨
ADMIN_PASSWORD = "1234" 

# --- 파일 경로 정의 (프로젝트 폴더 내에 저장) ---
MENTEE_FILE = 'mentee_data.csv'
MATCH_FILE = 'match_data.csv'

# ----------------------------------------------------------------------
# 헬퍼 함수: 파일 기반 데이터 처리
# ----------------------------------------------------------------------

def load_data(file_path, columns):
    """CSV 파일이 있으면 로드하고, 없거나 비어 있으면 빈 DataFrame을 기반으로 초기화합니다."""
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            # NA 처리 방지: '없음', 'N/A' 같은 문자열이 NaN으로 변환되는 것 방지
            df = pd.read_csv(file_path, keep_default_na=False) 
            return df.to_dict('records')
        except Exception:
            # 파일 읽기 오류 시 빈 데이터 구조 반환
            return pd.DataFrame(columns=columns).to_dict('records')
    # 파일이 없거나 비어 있을 때 초기화
    return pd.DataFrame(columns=columns).to_dict('records')

def save_data(data_list, file_path, columns):
    """데이터를 CSV 파일로 저장합니다."""
    df = pd.DataFrame(data_list, columns=columns)
    df.to_csv(file_path, index=False)

# ----------------------------------------------------------------------
# 페이지 상태 관리 및 초기화 (데이터 로드 포함)
# ----------------------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'signup_and_survey'
if 'survey_done' not in st.session_state:
    st.session_state.survey_done = False
if 'mentor_data' not in st.session_state:
    # 멘토 데이터는 앱이 실행되는 동안 메모리에 유지 (CSV로 저장하지 않음)
    st.session_state.mentor_data = [] 
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'current_mentor_id' not in st.session_state:
    st.session_state.current_mentor_id = None 
    
# 🌟 멘티 데이터 및 매칭 데이터 자동 로드 (CSV 파일 사용)
MENTEE_COLS = ['ID', '이름', '나이대', '목표', '관심 주제', '등록일', '매칭 상태']
MATCH_COLS = ['Match_ID', 'Mentor_ID', 'Mentor_Name', 'Mentee_ID', 'Mentee_Name', '매칭일', '상태']

st.session_state.mentee_data = load_data(MENTEE_FILE, MENTEE_COLS)
st.session_state.match_data = load_data(MATCH_FILE, MATCH_COLS)


# ----------------------------------------------------------------------
# 헬퍼 함수 
# ----------------------------------------------------------------------
def find_mentor_by_id(mentor_id):
    """ID로 멘토 객체를 찾아 반환합니다."""
    return next((m for m in st.session_state.mentor_data if m['ID'] == mentor_id), None)

def find_mentee_by_id(mentee_id):
    """ID로 멘티 객체를 찾아 반환합니다."""
    return next((m for m in st.session_state.mentee_data if m['ID'] == mentee_id), None)

def calculate_match_score(mentor_profile, mentee_profile):
    """
    멘토와 멘티 프로필을 비교하여 매칭 적합도 점수를 계산합니다.
    (간단한 키워드 일치 기반 점수화)
    """
    score = 0
    
    # 멘토의 문자열 목록 (쉼표로 구분됨)을 리스트로 변환
    mentor_topics = set(mentor_profile.get('주요 주제', '').split(', '))

    # 멘티의 문자열 목록을 리스트로 변환
    mentee_goals = set(mentee_profile.get('목표', '').split(', '))
    mentee_topics = set(mentee_profile.get('관심 주제', '').split(', '))
    
    # 1. 멘토 주제와 멘티 관심 주제 일치 시 (가장 중요)
    common_topics = mentor_topics.intersection(mentee_topics)
    score += len(common_topics) * 20 # 일치당 20점 부여

    # 2. 멘토링 목적과 멘티 목표 일치 시
    mentor_purposes_map = {
        '진로/커리어 조언': ['커리어 조언', '특정 기술 학습'],
        '학업/전문지식 조언': ['특정 기술 학습'],
        '사회/인생 경험 공유': ['인생 경험 공유'],
        '정서적 지지 및 대화': ['심리적 지지']
    }
    
    mentor_purpose_list = mentor_profile.get('멘토링 목적', '').split(', ')
    
    for purpose in mentor_purpose_list:
        if purpose in mentor_purposes_map:
            for goal in mentee_goals:
                if goal in mentor_purposes_map[purpose]:
                    score += 15 # 목적/목표 일치당 15점 부여
                   
    return score

# ----------------------------------------------------------------------
# CSS 스타일링 (글씨 크기만 적정 수준으로 확대 및 통일)
# ----------------------------------------------------------------------
st.markdown("""
<style>
    /* 폰트 크기 수정 START: 폰트 사이즈를 적정 수준(1.5rem)으로 통일 */
    
    /* 1. 기본 텍스트, 라벨, 상세 정보 값 등 모든 일반 텍스트 */
    .st-emotion-cache-183060u, /* st.markdown, st.write의 일반 텍스트 */
    .st-emotion-cache-1cyp687, /* 일반적인 div 컨테이너 텍스트 */
    .st-emotion-cache-16sx4w0, /* 라벨 텍스트 (input, selectbox 위) */
    .st-emotion-cache-11r9c4z, /* 버튼, 입력 필드 등 내부 텍스트 */
    .st-emotion-cache-19k721u, /* 기타 일반 텍스트 */
    div[data-testid="stText"],
    div[data-testid="stMarkdownContainer"] p,
    .stMarkdown p,
    .stMarkdown,
    body,
    label.st-emotion-cache-p2w958, 
    label.st-emotion-cache-16sx4w0,
    div[data-testid="stForm"] label,
    div[data-testid="stForm"] p {
        font-size: 1.5rem !important; /* 1.5rem (약 15pt~18pt)로 조정 */
        color: #e0e0e0 !important;
        line-height: 1.6; /* 가독성을 위해 줄 간격 확보 */
    }
    
    /* 2. Alert, Info, Warning 메시지 박스 텍스트 크기 */
    .stAlert {
        font-size: 1.4rem !important; 
    }
    
    /* 3. 입력 필드 내부 텍스트 크기 확대 (실제 사용자가 입력하는 글씨) */
    .st-emotion-cache-9ez29k > div > input, 
    .st-emotion-cache-9ez29k > div > textarea,
    .st-emotion-cache-9ez29k > div > div,
    input[data-testid="stTextInput"],
    textarea[data-testid="stTextInput"],
    div[data-testid="stSelectbox"] div[role="button"],
    div[data-testid="stMultiSelect"] div[role="button"] {
        font-size: 1.5rem !important;
    }
    
    /* 4. 버튼 텍스트 크기 확대 */
    .stButton > button {
        font-size: 1.3rem !important; 
        padding: 0.8rem 1.6rem !important; 
    }
    
    /* 폰트 크기 수정 END */
    
    
    /* 제목 크기 */
    h1 {
        font-size: 2.5rem !important; 
        color: #f7a300 !important;
        font-weight: bold;
    }
    h2 {
        font-size: 2.0rem !important; 
        color: #f7a300 !important;
        font-weight: bold;
    }
    h3 {
        font-size: 1.7rem !important; 
        color: #f7a300 !important;
    }
    
    /* 사이드바, 입력창, 버튼 배경색 (기존 설정 유지) */
    .st-emotion-cache-16sx4w0, .st-emotion-cache-q8s-b9p {
        background-color: #1e1e1e !important;
    }
    
    /* 상세 프로필 박스 스타일 (기존 설정 유지) */
    .detail-box {
        background-color: #282c34;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #f7a300;
        margin-bottom: 20px;
    }
    .detail-label {
        color: #e0e0e0;
        font-weight: bold;
        margin-bottom: 5px;
        display: block;
        font-size: 1.5rem !important; /* 글씨 크기 통일 */
    }
    .detail-value {
        color: #ffffff;
        margin-left: 15px;
        font-size: 1.5rem !important; /* 글씨 크기 통일 */
    }
</style>
""", unsafe_allow_html=True)


# 페이지 이동 함수
def set_page(page_name):
    st.session_state.page = page_name

# 사이드바 메뉴 
with st.sidebar:
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=50)
    st.title("멘토 전용 메뉴")
    st.markdown("---")
    if st.button("📝 회원가입/설문"): set_page('signup_and_survey')
    if st.button("👤 내 매칭"): set_page('my_matches')
    if st.button("🔎 멘티 찾기"): set_page('find_matches')
    st.markdown("---")
    if st.button("⚙️ 관리자 대시보드"): 
        st.session_state.admin_authenticated = False 
        set_page('admin_dashboard')
    st.markdown("---")
    st.info("※ 데모용: 데이터는 CSV 파일로 저장됩니다.")


# ----------------------------------------------------------------------
# 페이지 함수: 멘티 찾기 (멘티 등록 및 매칭)
# ----------------------------------------------------------------------
def find_matches():
    st.title("🔎 멘티 찾기")
    
    current_mentor_id = st.session_state.current_mentor_id
    if not current_mentor_id:
        st.warning("⚠️ 멘티를 찾으려면 먼저 '회원가입/설문' 페이지에서 프로필 등록을 완료해야 합니다.")
        st.info("💡 등록 완료 후 이 페이지를 다시 방문하면 멘티를 매칭할 수 있습니다.")
        return

    # 현재 멘토의 프로필을 불러옵니다.
    mentor_profile = find_mentor_by_id(current_mentor_id)
    if not mentor_profile:
        st.error("❌ 멘토 프로필 정보를 찾을 수 없습니다. 다시 가입해 주세요.")
        return

    st.markdown("### 1. 멘티 등록 (외부 앱 시뮬레이션)")
    st.write("외부 멘티 앱에서 가입한 멘티 데이터를 여기에 등록하여 매칭 후보로 만듭니다.")
    st.info(f"✨ **'{MENTEE_FILE}'** 파일에서 멘티 데이터를 **자동으로 불러옵니다.**")
    
    with st.expander("➕ 새로운 멘티 등록하기 (테스트용)", expanded=False):
        with st.form("mentee_signup_form", clear_on_submit=True):
            mentee_name = st.text_input("멘티 이름", key='mentee_name_val')
            mentee_age = st.selectbox("멘티 나이대", ["10대", "20대", "30대", "40대 이상"], key='mentee_age_val')
            mentee_goal = st.multiselect(
                "멘티의 멘토링 목표 (복수 선택)", 
                ["커리어 조언", "심리적 지지", "특정 기술 학습", "인생 경험 공유"],
                key='mentee_goal_val'
            )
            mentee_topic = st.multiselect(
                "멘티가 관심 있는 주제", 
                ["진로", "학업", "재테크", "취미", "대인관계"],
                key='mentee_topic_val'
            )
            mentee_submitted = st.form_submit_button("멘티 등록 완료")

            if mentee_submitted:
                if mentee_name and mentee_goal and mentee_topic:
                    mentee_profile = {
                        'ID': str(uuid.uuid4())[:8],
                        '이름': mentee_name,
                        '나이대': mentee_age,
                        '목표': ", ".join(mentee_goal),
                        '관심 주제': ", ".join(mentee_topic),
                        '등록일': datetime.date.today().strftime("%Y-%m-%d"),
                        '매칭 상태': '대기'
                    }
                    st.session_state.mentee_data.append(mentee_profile)
                    
                    # 멘티 데이터를 파일에 저장
                    save_data(st.session_state.mentee_data, MENTEE_FILE, MENTEE_COLS)
                    
                    st.success(f"✅ 멘티 **'{mentee_name}'** 님의 등록이 완료되었습니다! (ID: {mentee_profile['ID']})")
                    st.rerun()
                else:
                    st.error("❌ 멘티 이름, 목표, 주제를 모두 입력해야 합니다.")

    st.markdown("---")

    st.markdown("### 2. 매칭 가능한 멘티 추천 목록")
    
    # 🌟 멘토 프로필을 기반으로 멘티 매칭 점수 계산
    available_mentees = [m for m in st.session_state.mentee_data if m['매칭 상태'] == '대기']
    
    # 점수 계산 및 멘토 정보 추가
    scored_mentees = []
    for mentee in available_mentees:
        score = calculate_match_score(mentor_profile, mentee)
        mentee['매칭 점수'] = score
        scored_mentees.append(mentee)
        
    # 점수가 높은 순서로 정렬
    scored_mentees.sort(key=lambda x: x['매칭 점수'], reverse=True)

    if not scored_mentees:
        st.info("현재 매칭을 기다리는 멘티가 없습니다. 새로운 멘티를 등록해주세요.")
        return

    # 상위 10명만 표시 (선택 사항)
    top_mentees = scored_mentees[:10]

    df_mentees = pd.DataFrame(top_mentees)
    
    # '매칭 점수'를 포함하여 사용자에게 보여줍니다.
    df_display = df_mentees[['ID', '이름', '나이대', '목표', '관심 주제', '매칭 점수']]
    
    # 멘토에게 가장 잘 맞는 멘티가 상위에 표시되도록 안내합니다.
    st.success("✨ **멘토님의 프로필 설문을 기반으로 가장 적합한 멘티를 추천했습니다.**")
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.markdown("#### 🤝 매칭 신청하기")
    
    col_id, col_btn = st.columns([2, 1])
    with col_id:
        target_mentee_id = st.text_input("매칭할 멘티의 ID를 입력하세요.", key='target_mentee_id')
    
    with col_btn:
        st.markdown("##### ") 
        if st.button("매칭 신청", use_container_width=True):
            current_mentor_id = st.session_state.current_mentor_id
            mentor_profile = find_mentor_by_id(current_mentor_id)
            mentee_profile = find_mentee_by_id(target_mentee_id)

            if not mentor_profile:
                st.error("❌ 멘토 프로필 정보가 유효하지 않습니다. 다시 로그인/가입해 주세요.")
            elif not mentee_profile or mentee_profile['매칭 상태'] != '대기':
                st.error("❌ 유효하지 않은 멘티 ID이거나, 이미 매칭 중인 멘티입니다.")
            else:
                # 매칭 처리
                match_id = str(uuid.uuid4())[:8]
                match_record = {
                    'Match_ID': match_id,
                    'Mentor_ID': current_mentor_id,
                    'Mentor_Name': mentor_profile['이름'],
                    'Mentee_ID': target_mentee_id,
                    'Mentee_Name': mentee_profile['이름'],
                    '매칭일': datetime.date.today().strftime("%Y-%m-%d"),
                    '상태': '매칭 완료'
                }
                st.session_state.match_data.append(match_record)
                
                # 멘티 상태 업데이트 (파일 저장 전에 session state 업데이트)
                for m in st.session_state.mentee_data:
                    if m['ID'] == target_mentee_id:
                        m['매칭 상태'] = '매칭됨'
                        break
                        
                # 🌟 데이터 파일에 저장
                save_data(st.session_state.mentee_data, MENTEE_FILE, MENTEE_COLS)
                save_data(st.session_state.match_data, MATCH_FILE, MATCH_COLS)
                
                # 멘토 상태 업데이트 (선택 사항)
                if mentor_profile['매칭 상태'] == '매칭 대기':
                    mentor_profile['매칭 상태'] = '매칭 중'
                
                st.balloons()
                st.success(f"🎉 **{mentee_profile['이름']}** 님과의 매칭이 성공적으로 완료되었습니다! Match ID: {match_id}")
                st.info("이제 '내 매칭' 페이지에서 매칭 정보를 확인하고 소통을 시작하세요.")
                set_page('my_matches') # '내 매칭' 페이지로 이동
                st.rerun()

# ----------------------------------------------------------------------
# 페이지 함수: 내 매칭 (매칭된 멘티 확인)
# ----------------------------------------------------------------------
def my_matches():
    st.title("👤 내 매칭")
    st.write("현재 매칭된 멘티와의 소통 현황을 확인합니다.")
    
    current_mentor_id = st.session_state.current_mentor_id
    if not current_mentor_id:
        st.warning("⚠️ 매칭 정보를 확인하려면 먼저 프로필 등록을 완료해야 합니다.")
        return

    st.markdown("### 매칭된 멘티 목록")

    # 🌟 파일에서 로드된 매칭 기록을 사용
    my_matches_list = [
        match for match in st.session_state.match_data 
        if match['Mentor_ID'] == current_mentor_id and match['상태'] == '매칭 완료'
    ]

    if not my_matches_list:
        st.info("✅ 아직 매칭된 상대가 없습니다. '멘티 찾기' 페이지에서 멘티에게 매칭을 신청해 보세요.")
        return

    df_matches = pd.DataFrame(my_matches_list)
    df_display = df_matches[['Match_ID', 'Mentee_Name', 'Mentee_ID', '매칭일', '상태']]
    df_display.columns = ['매칭 ID', '멘티 이름', '멘티 ID', '매칭일', '상태'] 

    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("#### 💬 매칭된 멘티의 상세 프로필 보기")
    
    mentee_options = {match['멘티 이름']: match['Mentee_ID'] for match in my_matches_list}
    selected_mentee_name = st.selectbox("상세 정보를 볼 멘티를 선택하세요.", ["선택하세요"] + list(mentee_options.keys()))

    if selected_mentee_name != "선택하세요":
        selected_mentee_id = mentee_options[selected_mentee_name]
        # 🌟 파일에서 로드된 멘티 상세 정보를 사용
        mentee_detail = find_mentee_by_id(selected_mentee_id)
        
        if mentee_detail:
            st.subheader(f"🔍 멘티 상세 프로필 ({selected_mentee_name})")
            
            html_content = ""
            for key, value in mentee_detail.items():
                if key not in ['ID', '매칭 상태', '매칭 점수']:
                    html_content += f'<div class="detail-label">{key}:</div><div class="detail-value">{value}</div>'
            
            st.markdown(f'<div class="detail-box">{html_content}</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------
# 페이지 함수: 관리자 대시보드
# ----------------------------------------------------------------------
def admin_dashboard():
    st.title("⚙️ 관리자 대시보드")
    st.write("플랫폼 전체 회원 현황을 조회합니다.")
    st.markdown("---")
    
    # --- 관리자 인증 영역 ---
    if not st.session_state.admin_authenticated:
        st.subheader("🔑 관리자 인증")
        password = st.text_input("관리자 비밀번호를 입력해주세요.", type="password", key='admin_password_input')
        
        if st.button("로그인"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("✅ 인증 성공! 대시보드가 로드됩니다.")
                st.rerun() 
            else:
                st.error("❌ 비밀번호가 올바르지 않습니다.")
        
        st.markdown("---")
        return

    # --- 인증 성공 후 대시보드 내용 ---
    
    mentors = st.session_state.mentor_data
    st.subheader(f"👥 멘토 회원 목록 (총 {len(mentors)}명)")
    
    if not mentors:
        st.info("아직 가입된 멘토 회원이 없습니다. 회원가입 페이지에서 테스트로 등록해주세요.")
        return

    df_mentors = pd.DataFrame(mentors)
    display_columns = ['ID', '이름', '이메일', '가입일', '나이대', '성별', '현재 직종', '만남 방식', '소통 스타일', '매칭 상태']
    df_display = df_mentors[display_columns]

    # --------------------------------
    # 필터링/검색 UI
    # --------------------------------
    with st.expander("🔍 멘토 검색 및 필터링"):
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            search_term = st.text_input("이름, 이메일, 직종으로 검색", key='admin_search_term')
        with col_filter2:
            status_options = ['전체'] + sorted(df_mentors['매칭 상태'].unique().tolist())
            selected_status = st.selectbox("매칭 상태별 필터", status_options, key='admin_status_filter')

        df_filtered = df_display.copy()
        
        if search_term:
            df_filtered = df_filtered[
                df_filtered['이름'].astype(str).str.contains(search_term, case=False, na=False) |
                df_filtered['이메일'].astype(str).str.contains(search_term, case=False, na=False) |
                df_filtered['현재 직종'].astype(str).str.contains(search_term, case=False, na=False)
            ]
            
        if selected_status != '전체':
            df_filtered = df_filtered[df_filtered['매칭 상태'] == selected_status]

    
    st.markdown(f"**총 {len(df_filtered)}건**의 멘토 회원 정보가 표시됩니다. (**ID**를 확인하세요)")
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

    st.markdown("---")

    st.subheader("🛠️ 멘토 상세 정보 조회")
    
    col_id, col_button = st.columns([2, 1])
    
    with col_id:
        target_id = st.text_input("상세 프로필을 볼 멘토 ID를 입력하세요.", key='target_mentor_
