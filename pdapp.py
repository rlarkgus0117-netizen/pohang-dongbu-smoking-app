import streamlit as st
import json
import os

# 페이지 기본 설정 (파스텔톤 테마 및 아이콘 적용)
st.set_page_config(
    page_title="건강한 폐, 건강한 포동",
    page_icon="🫁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 포항동부초 3~6학년 학급별 정원 데이터 설정
CAPACITIES = {
    "3-1": 14, "3-2": 15,
    "4-1": 16, "4-2": 16,
    "5-1": 16, "5-2": 16,
    "6-1": 17, "6-2": 16
}

# 로컬 데이터 저장 경로 (배포 환경 호환을 위해 상대 경로로 수정)
DB_PATH = "pohang_dongbu_stats.json"

# 참여 데이터 로드 및 초기화 함수
def load_stats():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    
    # 데이터가 없을 시 초기값 생성
    default_data = {k: 0 for k in CAPACITIES.keys()}
    save_stats(default_data)
    return default_data

# 참여 데이터 저장 함수
def save_stats(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 실시간 참여 스탯 로드
stats = load_stats()

# 초등학생 눈높이에 맞춘 파스텔톤 컬러 및 큰 글씨(20px 이상) 스타일 정의 (CSS)
st.markdown("""
<style>
    /* 전체 배경 스타일 */
    .stApp {
        background-color: #F0F4FF;
        font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
    }
    
    /* 대문 타이틀 카드 */
    .main-title {
        text-align: center;
        color: #4A7C59;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 5px;
        background: linear-gradient(120deg, #E8F5E9, #C8E6C9);
        padding: 15px;
        border-radius: 20px;
        border: 3px dashed #81C784;
    }
    
    .subtitle {
        text-align: center;
        color: #555555;
        font-size: 18px;
        margin-bottom: 25px;
    }
    
    /* 질문 상자 디자인 */
    .question-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 18px;
        border-left: 8px solid #64B5F6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        font-size: 20px;
        font-weight: bold;
        color: #1A237E;
    }
    
    /* 파스텔톤 안내 안내판 */
    .info-card {
        background-color: #E3F2FD;
        border-radius: 15px;
        padding: 15px;
        border: 2px solid #BBDEFB;
        font-size: 18px;
        color: #0D47A1;
        margin-bottom: 20px;
    }
    
    /* 오답 경고용 연분홍 팝업 박스 */
    .popup-box {
        background-color: #FFEBEE;
        border-left: 6px solid #EF5350;
        padding: 15px;
        border-radius: 10px;
        color: #C62828;
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    /* 정답 성공용 연초록 팝업 박스 */
    .success-box {
        background-color: #E8F5E9;
        border-left: 6px solid #66BB6A;
        padding: 15px;
        border-radius: 10px;
        color: #2E7D32;
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 귀여운 미소 짓는 '폐' 일러스트 및 실시간 완료 인원 비례 하트 생성 함수 (SVG)
def render_lungs_svg(completed_count, max_capacity):
    # 하트가 배치될 예쁜 전용 좌표 모음 (최대 정원수까지 순서대로 배치)
    heart_positions = [
        (35, 75), (165, 75), (40, 110), (160, 110), (55, 140), (145, 140), 
        (75, 45), (125, 45), (30, 95), (170, 95), (60, 120), (140, 120),   
        (100, 30), (50, 50), (150, 50), (85, 155), (115, 155),              
        (80, 130), (120, 130), (70, 90), (130, 90), (100, 160)              
    ]
    
    count = min(completed_count, max_capacity)
    
    # 학생 수만큼 하트 그래픽 코드 생성
    hearts_markup = ""
    for i in range(count):
        x, y = heart_positions[i % len(heart_positions)]
        hearts_markup += f"""
        <g transform="translate({x-10}, {y-10}) scale(0.8)">
            <path d="M12,5 C10,1 4,1 2,5 C0,9 6,14 12,20 C18,14 24,9 22,5 C20,1 14,1 12,5 Z" fill="#FF4D6D" />
        </g>
        """
        
    svg = f"""
    <svg width="220" height="220" viewBox="0 0 200 200" style="display: block; margin: auto;">
        <!-- 배경 부드러운 초록 원 -->
        <circle cx="100" cy="100" r="85" fill="#E8F5E9" opacity="0.6"/>
        
        <!-- 기관지 줄기 -->
        <path d="M 100,15 L 100,55" stroke="#FFA4A2" stroke-width="12" stroke-linecap="round" fill="none"/>
        <path d="M 90,30 L 110,30 M 90,40 L 110,40" stroke="#FFFFFF" stroke-width="2"/>
        
        <!-- 왼쪽 폐엽 -->
        <path d="M100,55 C80,35 25,45 25,95 C25,145 75,165 100,145 Z" fill="#FFC1CC" stroke="#FF8093" stroke-width="4" stroke-linejoin="round"/>
        
        <!-- 오른쪽 폐엽 -->
        <path d="M100,55 C120,35 175,45 175,95 C175,145 125,165 100,145 Z" fill="#FFC1CC" stroke="#FF8093" stroke-width="4" stroke-linejoin="round"/>
        
        <!-- 웃는 눈망울 -->
        <path d="M 50,85 Q 57,78 64,85" fill="none" stroke="#2C3E50" stroke-width="3" stroke-linecap="round"/>
        <path d="M 136,85 Q 143,78 150,85" fill="none" stroke="#2C3E50" stroke-width="3" stroke-linecap="round"/>
        
        <!-- 수줍은 복숭아빛 볼터치 -->
        <circle cx="45" cy="98" r="7" fill="#FF8A80" opacity="0.7"/>
        <circle cx="155" cy="98" r="7" fill="#FF8A80" opacity="0.7"/>
        
        <!-- 동그랗게 활짝 웃는 귀여운 입 -->
        <path d="M 88,105 Q 100,120 112,105" fill="none" stroke="#2C3E50" stroke-width="3" stroke-linecap="round"/>
        
        <!-- 실시간 누적 하트 레이어 -->
        {hearts_markup}
    </svg>
    """
    return svg

# 상단 대문 및 대시보드 화면 연동 구성
col_title, col_btn = st.columns([3, 1])

with col_title:
    st.markdown('<div class="main-title">🍀 포동 포동 흡연예방 캠페인</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">1학기에 우리가 배웠던 내용을 퀴즈로 튼튼하게 복습해요!</div>', unsafe_allow_html=True)

# 실시간 상황판 활성화 여부 제어용 세션 데이터 정의
if "show_school_dashboard" not in st.session_state:
    st.session_state.show_school_dashboard = False

# [건강한 폐, 건강한 포동] 토글 버튼 배치
with col_btn:
    st.write("") 
    if st.button("🏫 건강한 폐, 건강한 포동", key="school_btn", help="학교 전체의 건강 상태 보러 가기"):
        st.session_state.show_school_dashboard = not st.session_state.show_school_dashboard
        st.rerun()

# ── [전체 학교 통합 대시보드 모드] ───────────────────────────────────────
if st.session_state.show_school_dashboard:
    st.markdown("### 🏫 [건강한 폐, 건강한 포동] 포항동부초 실시간 하트 지도")
    st.markdown("우리 학교 모든 학급 친구들의 금연 다짐 하트가 모여 거대한 포동이의 건강한 폐가 완성되고 있어요! ❤️")
    
    # 전교 기준 통계 산출
    total_completed = sum(stats.values())
    total_capacity = sum(CAPACITIES.values())
    global_percentage = (total_completed / total_capacity) * 100 if total_capacity > 0 else 0
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown(render_lungs_svg(total_completed, total_capacity), unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: #E91E63;'>포항동부초 누적 하트: {total_completed}개 / {total_capacity}개</h3>", unsafe_allow_html=True)
    
    with col_r:
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; border: 2px solid #E1BEE7; box-shadow: 2px 2px 8px rgba(0,0,0,0.05);">
            <h4 style="margin: 0; color: #4A148C;">🌟 포동이의 약속 진척도</h4>
            <p style="font-size: 32px; font-weight: bold; color: #E91E63; margin: 10px 0;">{global_percentage:.1f}% 달성!</p>
            <p style="color: #666; font-size: 15px;">포항동부초등학교 학생들이 담배 유혹을 거부하고 깨끗한 공기를 만드는 주인공으로 무럭무럭 자라나고 있습니다!</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    st.write("#### 👥 우리 학급별 하트 상황판")
    grid_cols = st.columns(2)
    
    for idx, (cls_name, cap) in enumerate(CAPACITIES.items()):
        done = stats.get(cls_name, 0)
        col = grid_cols[idx % 2]
        pct = (done / cap) * 100
        
        with col:
            st.markdown(f"""
            <div style="background-color: #FAFAFA; padding: 15px; border-radius: 12px; margin-bottom: 10px; border-left: 5px solid #FF4D6D; box-shadow: 1px 1px 4px rgba(0,0,0,0.05);">
                <span style="font-size: 18px; font-weight: bold; color: #333;">{cls_name[0]}학년 {cls_name[2]}반 </span>
                <span style="font-size: 16px; color: #FF4D6D; font-weight: bold;">(❤️ {done}/{cap}명)</span>
                <div style="background-color: #E0E0E0; border-radius: 10px; height: 10px; width: 100%; margin-top: 5px;">
                    <div style="background-color: #FF4D6D; height: 10px; border-radius: 10px; width: {pct}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    if st.button("🔙 다시 퀴즈 맞추러 가기", key="back_to_quiz"):
        st.session_state.show_school_dashboard = False
        st.rerun()
        
    st.stop()

# ── [개인별 학급 퀴즈 풀기 모드] ───────────────────────────────────────
if "selected_class" not in st.session_state:
    st.session_state.selected_class = None
if "selected_grade" not in st.session_state:
    st.session_state.selected_grade = None
if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

# Step 1: 학년 및 학급 선택 첫 화면
if st.session_state.selected_class is None or st.session_state.selected_grade is None:
    st.markdown("### 🖐️ 안녕 포동이 친구들! 학년과 반을 골라주세요")
    
    grade_opts = ["선택하기", "3학년", "4학년", "5학년", "6학년"]
    grade_sel = st.selectbox("🎈 몇 학년인가요?", grade_opts)
    
    if grade_sel != "선택하기":
        grade_num = int(grade_sel[0])
        class_opts = ["선택하기", "1반", "2반"]
        class_sel = st.selectbox("🏫 몇 반인가요?", class_opts)
        
        if class_sel != "선택하기":
            class_num = int(class_sel[0])
            class_key = f"{grade_num}-{class_num}"
            
            if st.button("출발하기! 🚀"):
                st.session_state.selected_grade = grade_num
                st.session_state.selected_class = class_key
                st.session_state.quiz_finished = False
                st.rerun()
    st.stop()

grade = st.session_state.selected_grade
class_id = st.session_state.selected_class

st.markdown(f"#### 👤 **{grade}학년 {class_id[2]}반** 친구가 학습하는 중입니다!")
PLEDGE_PHRASE = "나는 평생 담배를 피우지 않고, 건강한 어린이가 될 것을 약속합니다!"

# SENSE 학년별 퀴즈 구현 분기
if grade == 3:
    # 3학년 SENSE 2단계: 간접흡연 및 금연구역
    st.markdown("""
    <div class="info-card">
        🌱 <b>3학년 복습 테마:</b> 1학기 때 우리는 담배가 미치는 <b>사회적 영향(간접흡연과 금연구역)</b>을 배웠어요.<br/>
        간접흡연의 위험을 기억하고, 안전한 금연구역을 올바르게 선택해보아요!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="question-box">💡 1단계: 간접흡연 팩트체크 OX 퀴즈</div>', unsafe_allow_html=True)
    st.markdown("**Q1. 담배를 피우는 사람의 옷, 머리카락, 방 벽지에 묻어있는 담배 유해 물질(3차 간접흡연)은 숨만 쉬어도 우리 건강에 심각한 유해를 끼칩니다.**")
    q1_ans = st.radio("알맞은 대답을 골라주세요:", ["선택하기", "맞아요 (O)", "틀려요 (X)"], key="3_q1")
    
    if q1_ans == "틀려요 (X)":
        st.markdown("""
        <div class="popup-box">
            🚨 틀렸어요! 다시 한 번 생각해보세요.<br/>
            <b>정답은 [O] 입니다!</b> 담배를 직접 피우지 않고 방이나 밀폐된 옷 속의 먼지만 들이마셔도, 
            몸 안에 독성 물질이 고스란히 들어오는 무서운 '3차 간접흡연'이 발생합니다!
        </div>
        """, unsafe_allow_html=True)
    elif q1_ans == "맞아요 (O)":
        st.markdown('<div class="success-box">👏 정답이에요! 옷이나 가구에 묻어 남는 담배 유해물질은 오랫동안 주변 사람을 아프게 한답니다.</div>', unsafe_allow_html=True)

    st.write("")
    
    st.markdown('<div class="question-box">💡 2단계: 우리 동네의 법정 "금연구역" 찾기</div>', unsafe_allow_html=True)
    st.markdown("깨끗한 마을을 만들기 위해 법으로 담배를 절대 피우지 못하게 정해진 **'금연구역'**을 모두 선택해주세요!")
    
    cols = st.columns(3)
    c_school = cols[0].checkbox("🏫 학교 전체 구역", value=False)
    c_playground = cols[1].checkbox("🛝 어린이 놀이터", value=False)
    c_bus = cols[2].checkbox("🚌 버스 정류소", value=False)
    
    cols_2 = st.columns(3)
    c_hospital = cols_2[0].checkbox("🏥 병원 주변 구역", value=False)
    c_park = cols_2[1].checkbox("🌳 도시 놀이공원", value=False)
    c_smoking_room = cols_2[2].checkbox("🚬 흡연실 안방", value=False)
    
    if st.button("정답 확인하기! ✅", key="3_check_zones"):
        if c_school and c_playground and c_bus and c_hospital and c_park and not c_smoking_room:
            st.success("🎉 대단해요! 법으로 정해진 모든 아동 보호용 금연구역을 올바르게 구별해냈습니다!")
        else:
            st.markdown("""
            <div class="popup-box">
                🚨 어라? 틀렸거나 체크하지 못한 구역이 있네요!<br/>
                <b>학교 전체, 어린이 놀이터, 버스 정류소, 병원, 도시공원</b>은 어린이와 이웃을 간접흡연으로부터 지키기 위해 
                <b>법으로 지정된 절대 금연구역</b>입니다. 흡연실을 제외하고 모두 체크해보세요!
            </div>
            """, unsafe_allow_html=True)

elif grade == 4:
    # 4학년 SENSE 2단계: 중독의 실체와 뇌건강
    st.markdown("""
    <div class="info-card">
        🧠 <b>4학년 복습 테마:</b> 1학기 때 우리는 담배가 주는 <b>정신적 영향(중독의 뇌 유해성)</b>을 배웠어요.<br/>
        중독의 굴레를 어떻게 벗어날 수 있을지 탐구해봅시다.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="question-box">💡 1단계: 내 뇌를 유괴하는 중독 4단계 퍼즐</div>', unsafe_allow_html=True)
    st.markdown("아래 빈칸에 가장 알맞은 단어를 보기에서 골라 채워보세요!")
    st.markdown("*보기: 도파민, 니코틴, 중독*")
    
    cell1 = st.selectbox("1) 담배를 피우면 [?] 이라는 중독성 물질이 폐를 타고 빠르게 뇌로 가요.", ["보기 선택", "도파민", "니코틴", "중독"])
    cell2 = st.selectbox("2) 이 물질은 뇌에서 기분을 속여 가짜 행복 호르몬인 [?] 을 억지로 만들어내요.", ["보기 선택", "도파민", "니코틴", "중독"])
    cell3 = st.selectbox("3) 효과가 끝나면 엄청난 불안감이 찾아오고, 스스로 멈출 수 없는 [?] 상태가 돼요.", ["보기 선택", "도파민", "니코틴", "중독"])
    
    if cell1 != "보기 선택" or cell2 != "보기 선택" or cell3 != "보기 선택":
        if cell1 == "니코틴" and cell2 == "도파민" and cell3 == "중독":
            st.markdown('<div class="success-box">👏 정답입니다! 한 번 니코틴에 지배당하면 스스로의 생각으로 끊기 힘든 정신 질환인 중독 상태가 되므로, 애초에 손대지 않는 것이 최선입니다.</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="popup-box">
                🚨 정답이 매칭되지 않았습니다. 빈칸을 다시 맞춰볼까요?<br/>
                <b>1) 니코틴</b>: 중독을 일으키는 핵심 물질<br/>
                <b>2) 도파민</b>: 인위적으로 뇌를 흥분시켜 속이는 가짜 기쁨의 물질<br/>
                <b>3) 중독</b>: 내 의지로 극복할 수 없는 뇌의 고장 상태
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    
    st.markdown('<div class="question-box">💡 2단계: 내 뇌를 자극할 건강한 스트레스 해소책 고르기</div>', unsafe_allow_html=True)
    st.markdown("**담배나 다른 나쁜 물질 대신, 내 뇌의 주인이 되어 자연스럽고 무해하게 기분을 풀 수 있는 건전한 행동은 무엇일까요? (가장 좋지 않은 것 선택)**")
    q2_ans = st.radio("기분을 건강하게 풀어줄 활동이 전혀 아닌 것을 하나 골라주세요:", 
                      ["선택하기", "친구들과 땀나게 축구 및 신체활동 하기", "방에 박혀서 하루종일 밤새 스마트폰 게임하기", "좋아하는 악기나 노래 부르기"], key="4_q2")
    
    if q2_ans == "방에 박혀서 하루종일 밤새 스마트폰 게임하기":
        st.markdown('<div class="success-box">👏 빙고! 과도한 스마트폰 게임 역시 건강한 도파민 분비 방식이 아니라, 또 다른 자극적 중독을 만들어내므로 지양해야 합니다.</div>', unsafe_allow_html=True)
    elif q2_ans in ["친구들과 땀나게 축구 및 신체활동 하기", "좋아하는 악기나 노래 부르기"]:
        st.markdown("""
        <div class="popup-box">
            🚨 다른 답을 검토해보세요!<br/>
            신체 운동과 악기 연주는 뇌 건강을 아주 건전하게 발달시키는 대표적인 예방법입니다.
        </div>
        """, unsafe_allow_html=True)

elif grade == 5:
    # 5학년 SENSE 3단계: 담배광고의 진실 및 전자담배 해로움
    st.markdown("""
    <div class="info-card">
        🍭 <b>5학년 복습 테마:</b> 1학기 때 우리는 <b>담배광고 마케팅의 왜곡 진실</b>과 <b>신종 전자담배의 해로움</b>을 파악했어요.<br/>
        친구들의 현명하고 스마트한 두뇌로 유혹을 무너뜨려 보아요!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="question-box">💡 1단계: 귀여운 전자담배 디자인의 숨겨진 음모 분석</div>', unsafe_allow_html=True)
    st.markdown("**Q1. 담배회사들이 과일향(망고, 민트 등)을 첨가하고 장난감이나 USB 같은 멋진 디자인으로 신종 담배를 만드는 본질적인 이유는 무엇일까요?**")
    q1_ans = st.radio("담배회사들이 숨기고 있는 아주 영악한 상업적 왜곡 전략은?",
                      ["선택하기", "담배가 몸에 좋으니까 선행을 베풀려고", "초등학생들을 장기 고객으로 끌어들여 평생 중독시키기 위해", "환경오염을 줄이기 위한 친환경적인 제품이라서"], key="5_q1")
    
    if q1_ans == "초등학생들을 장기 고객으로 끌어들여 평생 중독시키기 위해":
        st.markdown('<div class="success-box">👏 완벽한 분석입니다! 담배회사들은 평생 담배를 사고 매출을 안겨줄 충성 중독자를 만들기 위해 아동과 청소년에게 친숙한 수법으로 눈속임을 씁니다.</div>', unsafe_allow_html=True)
    elif q1_ans in ["담배가 몸에 좋으니까 선행을 베풀려고", "환경오염을 줄이기 위한 친환경적인 제품이라서"]:
        st.markdown("""
        <div class="popup-box">
            🚨 정답이 아닙니다!<br/>
            담배회사는 오직 자신들의 영리 판매 목적을 위해 해로운 독극물 담배를 <b>무해하고 세련된 아이템인 것처럼 위장</b>하여 접근하고 있습니다.
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    st.markdown('<div class="question-box">💡 2단계: 신종 전자담배 가짜뉴스 분별하기</div>', unsafe_allow_html=True)
    st.markdown("**Q2. '전자담배는 타르 성분이 나오지 않고 단순한 깨끗한 과일향 수증기이므로, 내 몸이나 남에게 아무런 해가 되지 않고 냄새만 좋다'는 말은 참일까요 거짓일까요?**")
    q2_ans = st.radio("가장 올바른 팩트체크 결론을 선택해주세요:", ["선택하기", "진실 (True) - 해롭지 않다", "거짓 (False) - 엄청 해롭다"], key="5_q2")
    
    if q2_ans == "거짓 (False) - 엄청 해롭다":
        st.markdown('<div class="success-box">👏 정답입니다! 전자담배에는 포름알데히드, 아세트알데히드 등 1급 발암물질과 강력한 중독 물질인 니코틴이 연기 속 가득 포함되어 있어 똑같이 아주 치명적입니다.</div>', unsafe_allow_html=True)
    elif q2_ans == "진실 (True) - 해롭지 않다":
        st.markdown("""
        <div class="popup-box">
            🚨 이런! 속으시면 절대 안 됩니다!<br/>
            <b>거짓(False)입니다!</b> 전자담배의 연기는 그냥 수증기가 아니라 미세한 화학 물질 방울이며, 일반 담배보다 더 많은 다양한 독성 발암 화학 배출물이 가득 들어있어 폐포를 빠르게 파괴합니다.
        </div>
        """, unsafe_allow_html=True)

elif grade == 6:
    # 6학년 SENSE 3단계: 욕구 대처 및 실전 거절
    st.markdown("""
    <div class="info-card">
        🛡️ <b>6학년 복습 테마:</b> 1학기 때 우리는 흡연 욕구 및 또래 친구 유혹에 단호하게 대응하는 <b>4D 수칙</b>과 <b>3단계 실전 거절법</b>을 연습했어요.<br/>
        중학교 진학을 앞두고 내 몸을 지킬 건강 주권을 단련합시다!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="question-box">💡 1단계: 흡연 유혹 이겨내기! 4D 행동 요령 퍼즐</div>', unsafe_allow_html=True)
    st.markdown("유혹이 올 때, 또는 극심한 스트레스를 받을 때 뇌 과학을 이용해 극복하는 4D 대처 전략을 매칭해보세요.")
    
    d1 = st.selectbox("Delay (유혹 지연): 흡연 욕구가 치솟아도 몇 분만 꾹 참고 시간을 끌어볼까요?", ["선택하기", "5초", "5분", "5시간"])
    d2 = st.selectbox("Deep Breathing (심호흡): 이완 작용을 위해 들이마시는 숨쉬기 방법은?", ["선택하기", "천천히 숨을 깊이 들이마시고 내쉬기", "엄청 빠르고 얕게 헉헉거리며 숨쉬기"])
    d3 = st.selectbox("Drink Water (물 마시기): 입안을 청소하고 니코틴 배출을 돕기 위해?", ["선택하기", "탄산음료 마시기", "미지근한 맑은 물 천천히 마시기"])
    
    if d1 != "선택하기" or d2 != "선택하기" or d3 != "선택하기":
        if d1 == "5분" and d2 == "천천히 숨을 깊이 들이마시고 내쉬기" and d3 == "미지근한 맑은 물 천천히 마시기":
            st.markdown('<div class="success-box">👏 대단해요! 4D 전략은 보건의학계에서 인정한 최고의 욕구 통제 전략입니다!</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="popup-box">
                🚨 알맞지 않은 대처 행동이 있어요!<br/>
                <b>Delay</b>: 담배 욕구는 과학적으로 <b>5분</b>이 지나면 현저하게 소멸합니다.<br/>
                <b>Deep breathing</b>: 폐 건강을 지키며 <b>천천히 깊게 심호흡</b>을 함으로써 뇌 신경을 차분히 이완시킵니다.<br/>
                <b>Drink water</b>: 물은 입에 가득 고인 흡연 갈증 충동을 안전하게 씻어줍니다.
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    
    st.markdown('<div class="question-box">💡 2단계: 실전 상황 또래 유혹 돌파하기 (3단계 거절극)</div>', unsafe_allow_html=True)
    st.markdown("**'너네 형도 이거 해봤대! 몰래 옥상에서 딸기향 나는 거 피워보자, 아무도 몰라.' 하고 은밀히 유혹하는 상황!**")
    
    st.markdown("자신을 당당하게 방어하는 **'3단계 정석 거절법'**에 가장 알맞은 행동 순서를 선택해주세요!")
    q2_ans = st.radio("거절의 3단계 흐름으로 가장 올바른 순서는?",
                      ["선택하기", 
                       "1단계: 무조건 화를 버럭 낸다 ➔ 2단계: 상대방 가방을 뒤진다 ➔ 3단계: 도망간다",
                       "1단계: 거절의 의사를 명확히(No) ➔ 2단계: 유해 근거 설명(Reason) ➔ 3단계: 건전한 행동 대안 제시 후 자리 탈출(Alternative)"], key="6_q2")
    
    if q2_ans == "1단계: 거절의 의사를 명확히(No) ➔ 2단계: 유해 근거 설명(Reason) ➔ 3단계: 건전한 행동 대안 제시 후 자리 탈출(Alternative)":
        st.markdown('<div class="success-box">👏 완벽한 3단계 정석입니다! "난 싫어! (No) ➔ 전자담배도 일급 발암물질 중독약물이야 (Reason) ➔ 축구하러 가자, 난 교실 갈게 (Alternative)" 로 매끄럽게 거절해보세요!</div>', unsafe_allow_html=True)
    elif q2_ans == "1단계: 무조건 화를 버럭 낸다 ➔ 2단계: 상대방 가방을 뒤진다 ➔ 3단계: 도망간다":
        st.markdown("""
        <div class="popup-box">
            🚨 아이쿠! 그 방법은 갈등을 크게 만들 수 있어 위험해요!<br/>
            현명하게 친구를 설득하되 나 자신을 완벽하게 수호하는 <b>3단계 과학적 대안 거절 대사</b>를 선택해보세요.
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── [평생금연 결의 선언식 & 제출 연계 시스템] ───────────────────────────────────
st.markdown('<div class="question-box">🕊️ 3단계: 평생 금연 결의 선언식</div>', unsafe_allow_html=True)
st.write("마지막 마무리 단계입니다. 아래에 나타난 '금연 다짐 약속' 문장을 오타 없이 똑같이 하단 텍스트 창에 직접 입력하여 제출하면 공식적으로 평생금연서약서가 우리 반 폐 지도로 정식 등록됩니다!")

st.info(f"👉 **정확히 입력할 문장:**\n`{PLEDGE_PHRASE}`")

student_input = st.text_input("✍️ 문장을 똑같이 입력해주세요:", placeholder="여기에 글자를 천천히 정확히 입력하세요!")

# 학생 완료 데이터 실시간 반영 함수
def trigger_completion():
    stats[class_id] += 1
    save_stats(stats)
    st.session_state.quiz_finished = True

if student_input:
    if student_input.strip() == PLEDGE_PHRASE:
        if not st.session_state.quiz_finished:
            trigger_completion()
        
        st.balloons() # 정답 기념 축하 풍선
        st.markdown(f"""
        <div style="background-color: #E8F5E9; padding: 25px; border-radius: 20px; border: 3px solid #4CAF50; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-top: 15px;">
            <h3 style="color: #2E7D32; margin-top: 0; text-align: center;">🎉 평생금연선언 등록 성공!</h3>
            <p style="font-size: 18px; line-height: 1.6; color: #1B5E20; text-align: center;">
                <b>칭찬합니다! 아주 자랑스럽습니다!</b> 👏<br/>
                {class_id[0]}학년 {class_id[2]}반 친구의 건강하고 아름다운 약속이 성공적으로 이행되어 보건실 지도에 전송되었습니다.<br/>
                앞으로도 사랑하는 가족과 나 자신의 깨끗한 숨결을 지키는 멋진 인재로 자라나길 온 포동 선생님들이 응원합니다!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 학급별 폐 지도 시각화 렌더링
        class_capacity = CAPACITIES.get(class_id, 16)
        class_done = stats.get(class_id, 0)
        
        st.write("")
        st.markdown(f"<h3 style='text-align: center;'>🫁 [폐가 건강한 우리 반] — {class_id[0]}학년 {class_id[2]}반 상황</h3>", unsafe_allow_html=True)
        st.markdown(render_lungs_svg(class_done, class_capacity), unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; font-size: 18px; font-weight: bold; color: #E91E63; margin-top: 10px;">
            현재 우리 반 하트 폐 완성도: {class_done}명 / {class_capacity}명 ({ (class_done/class_capacity)*100:.1f}%) 완료!<br/>
            하트 붉은 반점이 폐 주위를 소중하고 맑게 둘러싸고 있습니다. ❤️
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 처음으로 돌아가서 다른 친구 퀴즈 풀기"):
            st.session_state.selected_class = None
            st.session_state.selected_grade = None
            st.session_state.quiz_finished = False
            st.rerun()
    else:
        st.markdown("""
        <div class="popup-box">
            🚨 오타나 띄어쓰기 틀린 부분이 있어요! 마침표(!)까지 한 자 한 자 똑같아야 다짐이 정식 승인되어 보전됩니다. 다시 한 번 정확하게 적어주세요.
        </div>
        """, unsafe_allow_html=True)
