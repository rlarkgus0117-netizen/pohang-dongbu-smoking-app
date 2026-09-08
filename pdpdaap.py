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

# 로컬 데이터 저장 경로 (배포 환경 호환을 위해 상대 경로 사용)
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
    
    /* 다시 한 번 생각해보세요 노란색 알림 박스 */
    .retry-box {
        background-color: #FFFDE7;
        border-left: 6px solid #FBC02D;
        padding: 15px;
        border-radius: 10px;
        color: #F57F17;
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

# 퀴즈 제출 관리 헬퍼 함수 (2단계 기회 룰 반영)
def check_quiz_answer(key, current_val, correct_val, is_ready):
    if "attempts" not in st.session_state:
        st.session_state.attempts = {}
    if "last_val" not in st.session_state:
        st.session_state.last_val = {}
        
    if not is_ready:
        return "none"
        
    last = st.session_state.last_val.get(key, None)
    if current_val != last:
        st.session_state.last_val[key] = current_val
        if current_val != correct_val:
            st.session_state.attempts[key] = st.session_state.attempts.get(key, 0) + 1
        else:
            st.session_state.attempts[key] = 0  # 정답 시 시도횟수 리셋
            
    attempts = st.session_state.attempts.get(key, 0)
    if current_val == correct_val:
        return "correct"
    else:
        if attempts == 1:
            return "retry"  # 1차 오답 -> "다시 한번 생각해보세요"
        else:
            return "failed"  # 2차 오답 -> 최종 정답 및 해설 공개

# 상단 대문 구성
col_title, col_btn = st.columns([3, 1])

with col_title:
    st.markdown('<div class="main-title">🍀 포동 포동 흡연예방 캠페인</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">1학기에 우리가 배웠던 내용을 재미있게 복습해요!</div>', unsafe_allow_html=True)

# 실시간 상황판 활성화 여부 제어용 세션 데이터 정의
if "show_school_dashboard" not in st.session_state:
    st.session_state.show_school_dashboard = False

# [건강한 폐, 건강한 포동] 대시보드 토글 버튼 배치
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
if "quiz_step" not in st.session_state:
    st.session_state.quiz_step = 1
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
                st.session_state.quiz_step = 1
                st.session_state.quiz_finished = False
                st.rerun()
    st.stop()

grade = st.session_state.selected_grade
class_id = st.session_state.selected_class
step = st.session_state.quiz_step

st.markdown(f"#### 👤 **{grade}학년 {class_id[2]}반** 친구가 학습하는 중입니다!")
PLEDGE_PHRASE = "나는 평생 담배를 피우지 않고, 건강한 어린이가 될 것을 약속합니다!"

# SENSE 학년별 퀴즈 구현 분기 (한 페이지에 딱 1문제씩만 노출되도록 제어)

# ── 3학년 영역 ────────────────────────────────────────────────────────
if grade == 3:
    if step == 1:
        st.markdown("""
        <div class="info-card">
            🌱 <b>3학년 복습 테마 (1단계):</b> 1학기 때 배운 담배의 <b>사회적 영향(간접흡연의 위험)</b>을 기억해봅시다!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="question-box">💡 1단계 문제: 간접흡연 팩트체크 OX 퀴즈</div>', unsafe_allow_html=True)
        st.markdown("**담배를 피우는 사람의 옷, 머리카락, 방 벽지에 유해 물질이 묻어 남는 것(3차 간접흡연)은 주변 사람의 건강에 해롭지 않다?**")
        q1_ans = st.radio("알맞은 대답을 골라주세요:", ["선택하기", "그렇다 (O) - 해롭지 않다", "아니다 (X) - 묻어 남은 연기도 아주 해롭다"], key="3_q1")
        
        q1_status = check_quiz_answer("3_q1", q1_ans, "아니다 (X) - 묻어 남은 연기도 아주 해롭다", q1_ans != "선택하기")
        
        if q1_status == "retry":
            st.markdown('<div class="retry-box">🤔 <b>다시 한번 생각해보세요!</b><br/>담배를 직접 피우지 않아도 옷이나 가구에 묻은 보이지 않는 해로운 입자는 어떻게 작용할까요? 다시 골라보세요!</div>', unsafe_allow_html=True)
        elif q1_status == "failed":
            st.markdown("""
            <div class="popup-box">
                🚨 <b>아쉬워요! 틀렸어요. 정답을 보여드릴게요!</b><br/>
                <b>정답은 [아니다 (X)] 입니다!</b><br/>
                직접 연기를 들이마시지 않고, 담배 연기가 밴 벽지, 카펫, 옷 등의 유해 물질을 마시는 것도 심각한 질병을 유발하는 <b>'3차 간접흡연'</b>이 발생합니다.
            </div>
            """, unsafe_allow_html=True)
            if st.button("다음 문제로 가기 ➔"):
                st.session_state.quiz_step = 2
                st.rerun()
        elif q1_status == "correct":
            st.markdown('<div class="success-box">👏 정답이에요! 옷이나 벽지에 남은 눈에 보이지 않는 타르 등의 독성 입자도 주변 사람들에게 매우 유해합니다.</div>', unsafe_allow_html=True)
            if st.button("다음 문제로 가기 ➔"):
                st.session_state.quiz_step = 2
                st.rerun()

    elif step == 2:
        st.markdown("""
        <div class="info-card">
            🌱 <b>3학년 복습 테마 (2단계):</b> 우리를 간접흡연으로부터 지켜주는 안전 구역을 알아볼까요?
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="question-box">💡 2단계 문제: 우리 동네의 "금연구역" 표시 모두 찾기</div>', unsafe_allow_html=True)
        st.markdown("우리 동네에서 법으로 정해져 담배를 절대 피우면 안 되는 **'금연구역'**을 모두 골라보세요!")
        
        cols = st.columns(3)
        c_school = cols[0].checkbox("🏫 학교 전체 운동장 및 실내", value=False)
        c_playground = cols[1].checkbox("🛝 어린이 놀이터", value=False)
        c_bus = cols[2].checkbox("🚌 버스 정류소 주변", value=False)
        
        cols_2 = st.columns(3)
        c_hospital = cols_2[0].checkbox("🏥 병원 주변 구역", value=False)
        c_park = cols_2[1].checkbox("🌳 도시 놀이공원", value=False)
        c_smoking_room = cols_2[2].checkbox("🚬 전용 흡연 부스 내부", value=False)
        
        if "zones_attempts" not in st.session_state:
            st.session_state.zones_attempts = 0
        if "zones_checked" not in st.session_state:
            st.session_state.zones_checked = False
            
        if st.button("정답 확인하기! ✅"):
            st.session_state.zones_checked = True
            is_correct = (c_school and c_playground and c_bus and c_hospital and c_park and not c_smoking_room)
            if is_correct:
                st.session_state.zones_attempts = 0
            else:
                st.session_state.zones_attempts += 1
                
        if st.session_state.zones_checked:
            is_correct = (c_school and c_playground and c_bus and c_hospital and c_park and not c_smoking_room)
            if is_correct:
                st.markdown('<div class="success-box">👏 완벽하게 찾아냈어요! 법정 금연구역은 간접흡연 피해를 완전히 차단하기 위해 엄격히 지켜집니다.</div>', unsafe_allow_html=True)
                if st.button("다짐 선언하러 가기 ➔"):
                    st.session_state.quiz_step = 3
                    st.rerun()
            else:
                attempts = st.session_state.zones_attempts
                if attempts == 1:
                    st.markdown('<div class="retry-box">🤔 <b>다시 한번 생각해보세요!</b><br/>틀렸거나 아직 체크하지 않은 곳이 있어요. 어린이와 시민들의 건강이 안전하게 보장되어야 하는 장소를 다시 확인해보세요.</div>', unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="popup-box">
                        🚨 <b>틀렸어요. 정답을 공개할게요!</b><br/>
                        <b>학교, 어린이 놀이터, 버스 정류소, 병원, 도시공원</b>은 법정 금연구역입니다. (흡연실은 흡연이 허용된 곳이므로 제외합니다.)
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("다짐 선언하러 가기 ➔"):
                        st.session_state.quiz_step = 3
                        st.rerun()

# ── 4학년 영역 ────────────────────────────────────────────────────────
elif grade == 4:
    if step == 1:
        st.markdown("""
        <div class="info-card">
            🧠 <b>4학년 복습 테마 (1단계):</b> 담배가 뇌에 주는 <b>정신적 유해 영향인 '중독'</b>을 복습해봅시다!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="question-box">💡 1단계 문제: 내 소중한 뇌를 망가뜨리는 중독 순환 퍼즐</div>', unsafe_allow_html=True)
        st.markdown("보기의 단어를 알맞게 골라 뇌의 납치 과정을 완성해보세요! (보기: 니코틴, 도파민, 중독)")
        
        cell1 = st.selectbox("1) 담배를 피우면 [?] 이라는 자극성 물질이 뇌로 유입돼요.", ["선택하기", "도파민", "니코틴", "중독"])
        cell2 = st.selectbox("2) 이 물질이 행복을 느끼게 하는 기분 물질인 [?] 을 억지로 가짜 분비하게 만들어요.", ["선택하기", "도파민", "니코틴", "중독"])
        cell3 = st.selectbox("3) 시간이 흘러 약효가 떨어지면 오히려 극심한 불안감이 오며 스스로 끊지 못하는 [?] 에 빠집니다.", ["선택하기", "도파민", "니코틴", "중독"])
        
        is_ready = (cell1 != "선택하기" and cell2 != "선택하기" and cell3 != "선택하기")
        q1_status = check_quiz_answer("4_q1", (cell1, cell2, cell3), ("니코틴", "도파민", "중독"), is_ready)
        
        if q1_status == "retry":
            st.markdown('<div class="retry-box">🤔 <b>다시 한번 생각해보세요!</b><br/>담배 속 핵심 유해물질 이름과 가짜 쾌감을 주는 호르몬의 이름을 알맞게 매칭했는지 다시 한 번 짚어보세요.</div>', unsafe_allow_html=True)
        elif q1_status == "failed":
            st.markdown("""
            <div class="popup-box">
                🚨 <b>아쉬워요! 틀렸어요. 정답을 보여드릴게요!</b><br/>
                <b>1) 니코틴</b>: 중독을 일으키는 대표 성분<br/>
                <b>2) 도파민</b>: 뇌를 인위적으로 유혹해 가짜 기쁨 물질<br/>
                <b>3) 중독</b>: 내 의지로 멈출 수 없는 뇌의 고장 상태
            </div>
            """, unsafe_allow_html=True)
            if st.button("다음 문제로 가기 ➔"):
                st.session_state.quiz_step = 2
                st.rerun()
        elif q1_status == "correct":
            st.markdown('<div class="success-box">👏 정답입니다! 한 번 고장난 중독 뇌 회로는 본인의 의지로 치유되기 어렵기 때문에, 애초에 손대지 않는 것이 최선입니다!</div>', unsafe_allow_html=True)
            if st.button("다음 문제로 가기 ➔"):
                st.session_state.quiz_step = 2
                st.rerun()

    elif step == 2:
        st.markdown("""
        <div class="info-card">
            🧠 <b>4학년 복습 테마 (2단계):</b> 내 뇌의 주인이 되어 자연스럽게 스트레스를 풀 수 있는 건강한 방법을 찾아보세요.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="question-box">💡 2단계 문제: 뇌 건강을 살려주는 안전한 스트레스 해소법이 아닌 것은?</div>', unsafe_allow_html=True)
        q2_ans = st.radio("가장 올바르지 않은 자극적 취미 활동을 하나 선택하세요:", 
                          ["선택하기", "친구들과 신나게 운동장을 달리며 신체활동 하기", "방 안에서 밤이 새도록 눈 아프게 자극적인 스마트폰 게임만 집중적으로 하기", "자신이 좋아하는 평온한 악기 연주나 노래 부르기"], key="4_q2")
        
        q2_status = check_quiz_answer("4_q2", q2_ans, "방 안에서 밤이 새도록 눈 아프게 자극적인 스마트폰 게임만 집중적으로 하기", q2_ans != "선택하기")
        
        if q2_status == "retry":
            st.markdown('<div class="retry-box">🤔 <b>다시 한번 생각해보세요!</b><br/>신체 활동과 음악은 도파민을 건강하게 분비하도록 돕습니다. 뇌을 계속 피로하게 만드는 유해 행동이 무엇인지 골라보세요!</div>', unsafe_allow_html=True)
        elif q2_status == "failed":
            st.markdown("""
            <div class="popup-box">
                🚨 <b>틀렸습니다. 정답을 보여드릴게요!</b><br/>
                <b>정답은 [방 안에서 밤이 새도록 눈 아프게 자극적인 스마트폰 게임만 집중적으로 하기] 입니다.</b><br/>
                과도하고 불규칙한 디지털 게임 역시 기형적인 가짜 행복 호르몬을 분비하게 만들어 또 다른 중독 회로를 유발하므로 정화가 필요합니다.
            </div>
            """, unsafe_allow_html=True)
            if st.button("다짐 선언하러 가기 ➔"):
                st.session_state.quiz_step = 3
                st.rerun()
        elif q2_status == "correct":
            st.markdown('<div class="success-box">👏 정답입니다! 자극적인 미디어 중독에서 벗어나 몸과 정신이 함께 자라나는 생산적인 스포츠와 예술 활동으로 일상을 채우는 것이 최선입니다.</div>', unsafe_allow_html=True)
            if st.button("다짐 선언하러 가기 ➔"):
                st.session_state.quiz_step = 3
                st.rerun()

# ── 5학년 영역 ────────────────────────────────────────────────────────
elif grade == 5:
    if step == 1:
        st.markdown("""
        <div class="info-card">
            🍭 <b>5학년 복습 테마 (1단계):</b> 달콤한 눈속임 속 <b>담배회사의 상업 왜곡 마케팅</b>을 꿰뚫어봅시다!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="question-box">💡 1단계 문제: 향긋하고 예쁜 신종 담배의 교묘한 속셈</div>', unsafe_allow_html=True)
        st.markdown("**담배회사들이 알록달록한 디자인과 달콤한 과일 향(망고, 청포도 등)을 첨가해 신종 담배를 꾸준히 개발해내는 이유는 무엇일까요?**")
        q1_ans = st.radio("가장 정답에 가까운 목적을 하나 골라주세요:",
                          ["선택하기", "어린이와 청소년의 입맛에 배려 혜택을 제공하기 위해서", "어린 나이부터 쉽게 접근하게 만들어 평생 담배를 사주는 중독 고객으로 가두기 위해", "자연 분해가 빠르고 인체 무해한 영양 공급원으로 만들기 위해"], key="5_q1")
        
        q1_status = check_quiz_answer("5_q1", q1_ans, "어린 나이부터 쉽게 접근하게 만들어 평생 담배를 사주는 중독 고객으로 가두기 위해", q1_ans != "선택하기")
        
        if q1_status == "retry":
            st.markdown('<div class="retry-box">🤔 <b>다시 한번 생각해보세요!</b><br/>상업 회사가 독극물 상품을 세련되게 꾸미는 이면에 감춰진 차가운 진실이 무엇일지 다시 한 번 생각해보세요.</div>', unsafe_allow_html=True)
        elif q1_status == "failed":
            st.markdown("""
            <div class="popup-box">
                🚨 <b>아쉬워요! 정답을 보여드릴게요!</b><br/>
                <b>정답은 [어린 나이부터 쉽게 접근하게 만들어 평생 담배를 사주는 중독 고객으로 가두기 위해] 입니다!</b><br/>
                귀여운 향과 형태의 담배는 어린이의 거부감을 없애고 마케팅의 노예로 전락시키기 위한 교묘한 눈속임 상술에 불과합니다.
            </div>
            """, unsafe_allow_html=True)
            if st.button("다음 문제로 가기 ➔"):
                st.session_state.quiz_step = 2
                st.rerun()
        elif q1_status == "correct":
            st.markdown('<div class="success-box">👏 역시 똑똑한 5학년이네요! 예쁘고 화려한 디자인에 절대 마음을 속여 빼앗기지 않는 주체적인 마음가짐을 기억합시다!</div>', unsafe_allow_html=True)
            if st.button("다음 문제로 가기 ➔"):
                st.session_state.quiz_step = 2
                st.rerun()

    elif step == 2:
        st.markdown("""
        <div class="info-card">
            🍭 <b>5학년 복습 테마 (2단계):</b> 전자담배에 대한 무서운 거짓 정보를 팩트로 격파해봅시다!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="question-box">💡 2단계 문제: 신종 전자담배 팩트체크 진실 공방</div>', unsafe_allow_html=True)
        st.markdown("**'전자담배 연기는 타르가 나오지 않고 단순히 향기 가득한 깨끗한 수증기일 뿐이므로, 나의 몸이나 주변인에게 간접 유해가 전혀 없다'는 말은 맞을까요?**")
        q2_ans = st.radio("진실 여부를 판가름하여 골라주세요:", ["선택하기", "그렇다 (참) - 연기는 깨끗한 수증기이다", "아니다 (거짓) - 일급 발암물질과 니코틴 약물이 가득하다"], key="5_q2")
        
        q2_status = check_quiz_answer("5_q2", q2_ans, "아니다 (거짓) - 일급 발암물질과 니코틴 약물이 가득하다", q2_ans != "선택하기")
        
        if q2_status == "retry":
            st.markdown('<div class="retry-box">🤔 <b>다시 한번 생각해보세요!</b><br/>수증기라는 명칭 뒤에 숨겨진 독성 미세 화학 방울 입자들을 과학적으로 배웠던 사실을 잊지 마세요! 다시 결정해 볼까요?</div>', unsafe_allow_html=True)
        elif q2_status == "failed":
            st.markdown("""
            <div class="popup-box">
                🚨 <b>아쉬워요! 틀렸습니다. 정답을 보여드릴게요!</b><br/>
                <b>정답은 [아니다 (거짓) - 일급 발암물질과 니코틴 약물이 가득하다] 입니다.</b><br/>
                신종 전자담배 연기는 물 수증기가 결코 아니며, 미세먼지뿐만 아니라 포름알데히드, 아세트알데히드 등 유해 1급 발암물질이 배출되어 폐와 기도를 심하게 오염시킵니다.
            </div>
            """, unsafe_allow_html=True)
            if st.button("다짐 선언하러 가기 ➔"):
                st.session_state.quiz_step = 3
                st.rerun()
        elif q2_status == "correct":
            st.markdown('<div class="success-box">👏 정답입니다! 전자담배도 담배잎의 독한 유독 입자들과 발암 화학 결합물이 다량 내포되어 있어, 간접 연기 흡입 시에도 똑같이 아주 해롭습니다.</div>', unsafe_allow_html=True)
            if st.button("다짐 선언하러 가기 ➔"):
                st.session_state.quiz_step = 3
                st.rerun()

# ── 6학년 영역 ────────────────────────────────────────────────────────
elif grade == 6:
    if step == 1:
        st.markdown("""
        <div class="info-card">
            🛡️ <b>6학년 복습 테마 (1단계):</b> 유혹 충동이 찾아올 때 의과학적인 수칙으로 극복하는 <b>대처 요령 4가지</b>를 익혀봅시다!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="question-box">💡 1단계 문제: 보건의학 표준 극복 행동 강령 퀴즈</div>', unsafe_allow_html=True)
        st.markdown("유혹이 올 때, 또는 극심한 스트레스를 받을 때 뇌 과학을 이용해 극복하는 행동 수칙을 알맞게 짝지어보세요.")
        
        d1 = st.selectbox("1) 유혹 충동 지연: 충동은 뇌 속에서 잠깐 활성화되었다가 가라앉아요. 몇 분만 꾹 참아볼까요?", ["선택하기", "5초만 버티기", "5분만 참고 기다리기", "5시간 동안 도망치기"])
        d2 = st.selectbox("2) 이완 호흡 요령: 뇌 신경을 차분하게 진정시키기 위한 부드러운 숨쉬기는?", ["선택하기", "부드럽고 아주 깊게 심호흡하기", "엄청 빠르고 얕게 헉헉거리며 숨쉬기"])
        d3 = st.selectbox("3) 건강한 수분 섭취: 입안을 정화하고 갈증 충동을 가라앉히기 위해?", ["선택하기", "탄산음료 마시기", "미지근하고 맑은 깨끗한 물 천천히 마시기"])
        
        is_ready = (d1 != "선택하기" and d2 != "선택하기" and d3 != "선택하기")
        q1_status = check_quiz_answer("6_q1", (d1, d2, d3), ("5분만 참고 기다리기", "부드럽고 아주 깊게 심호흡하기", "미지근하고 맑은 깨끗한 물 천천히 마시기"), is_ready)
        
        if q1_status == "retry":
            st.markdown('<div class="retry-box">🤔 <b>다시 한번 생각해보세요!</b><br/>우리 몸의 순환 체계를 가장 안전하게 이완시켜줄 시간과 숨쉬기 요령, 그리고 마시는 수분을 잘 결합해보세요.</div>', unsafe_allow_html=True)
        elif q1_status == "failed":
            st.markdown("""
            <div class="popup-box">
                🚨 <b>틀렸어요. 정답 매칭을 보여드릴게요!</b><br/>
                <b>1) 충동 지연</b>: 흡연 충동은 약 <b>5분</b>만 참으면 현저하게 약해집니다.<br/>
                <b>2) 이완 호흡</b>: 부드럽고 <b>깊게 심호흡</b>을 하며 몸을 진정시킵니다.<br/>
                <b>3) 수분 섭취</b>: 탄산음료 대신 <b>맑은 깨끗한 물</b>을 천천히 들이켜 씻어냅니다.
            </div>
            """, unsafe_allow_html=True)
            if st.button("다음 문제로 가기 ➔"):
                st.session_state.quiz_step = 2
                st.rerun()
        elif q1_status == "correct":
            st.markdown('<div class="success-box">👏 대단해요! 보건의학계에서 인정한 최고의 욕구 통제 전략입니다!</div>', unsafe_allow_html=True)
            if st.button("다음 문제로 가기 ➔"):
                st.session_state.quiz_step = 2
                st.rerun()

    elif step == 2:
        st.markdown("""
        <div class="info-card">
            🛡️ <b>6학년 복습 테마 (2단계):</b> 예비 중학생으로서 맞닥뜨릴 실전 권유 상황을 지혜롭게 차단해 봅시다!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="question-box">💡 2단계 문제: 실전! 유혹 권유 차단하는 단호한 거절 3단계</div>', unsafe_allow_html=True)
        st.markdown("**'아무도 보지 않는 놀이터에서 가장 친한 단짝 친구가 과일 향 전자기기를 권하며 몰래 같이 해보자고 할 때'**")
        
        q2_ans = st.radio("친구 관계도 부드럽게 지키며, 나 자신을 단호히 지키는 올바른 3단계 수칙의 배치는?",
                          ["선택하기", 
                           "무조건 화를 버럭 낸다 ➔ 친구의 주머니와 가방을 강제로 뒤진다 ➔ 경찰서에 이른다고 위협하며 도망치기",
                           "1단계: 단호하게 사양하기 (No) ➔ 2단계: 신체에 아주 유해하다는 근거 설명하기 (Reason) ➔ 3단계: 다른 재미있는 대안 활동을 제안하며 자리에서 멀어지기 (Alternative)"], key="6_q2")
        
        q2_status = check_quiz_answer("6_q2", q2_ans, "1단계: 단호하게 사양하기 (No) ➔ 2단계: 신체에 아주 유해하다는 근거 설명하기 (Reason) ➔ 3단계: 다른 재미있는 대안 활동을 제안하며 자리에서 멀어지기 (Alternative)", q2_ans != "선택하기")
        
        if q2_status == "retry":
            st.markdown('<div class="retry-box">🤔 <b>다시 한번 생각해보세요!</b><br/>감정적인 다툼을 최소화하면서도, 주관 있는 태도로 의사를 표현하는 거절의 황금 법칙을 다시 골라보세요.</div>', unsafe_allow_html=True)
        elif q2_status == "failed":
            st.markdown("""
            <div class="popup-box">
                🚨 <b>아쉬워요! 틀렸습니다. 정답을 보여드릴게요!</b><br/>
                <b>정답은 [1단계: 사양하기 ➔ 2단계: 근거 설명 ➔ 3단계: 대안 제안 및 탈출] 흐름입니다.</b><br/>
                화를 무작정 내는 대응은 대화를 파국으로 만들 수 있습니다. 부드럽지만 당당하게(No) 거절하고 해로움을 말하며(Reason), 다른 활동을 하도록 이끄는 것(Alternative)이 예비 중학생 필수 소양입니다.
            </div>
            """, unsafe_allow_html=True)
            if st.button("다짐 선언하러 가기 ➔"):
                st.session_state.quiz_step = 3
                st.rerun()
        elif q2_status == "correct":
            st.markdown('<div class="success-box">👏 완벽합니다! "난 하지 않을래! ➔ 전자담배도 일급 발암물질이 들어있거든 ➔ 농구 한 판 하거나 오락실 갈까? 난 먼저 갈게!" 처럼 현명하게 대처해내실 것입니다!</div>', unsafe_allow_html=True)
            if st.button("다짐 선언하러 가기 ➔"):
                st.session_state.quiz_step = 3
                st.rerun()

# ── [평생금연 결의 선언식 & 제출 연계 시스템 - 3단계 공통] ───────────────────────────────────
if step == 3:
    st.markdown('<div class="question-box">🕊️ 3단계: 평생 금연 약속 선언식</div>', unsafe_allow_html=True)
    st.write("마지막 마무리 단계입니다. 아래에 나타난 '금연 다짐 약속' 문장을 오타나 빈칸 띄어쓰기 없이 똑같이 하단 입력창에 타이핑하여 등록하면, 공식적으로 평생금연서약서가 우리 반 폐 지도로 제출됩니다!")
    
    st.info(f"👉 **정확히 입력할 문장:**\n`{PLEDGE_PHRASE}`")
    
    student_input = st.text_input("✍️ 문장을 똑같이 입력해주세요:", placeholder="여기에 글자를 차분하게 정확히 입력해 주세요!")
    
    # 학생 완료 데이터 실시간 저장 및 갱신 함수
    def trigger_completion():
        stats[class_id] += 1
        save_stats(stats)
        st.session_state.quiz_finished = True
        
    if student_input:
        if student_input.strip() == PLEDGE_PHRASE:
            if not st.session_state.quiz_finished:
                trigger_completion()
                
            st.balloons()  # 축하 오색 풍선
            st.markdown(f"""
            <div style="background-color: #E8F5E9; padding: 25px; border-radius: 20px; border: 3px solid #4CAF50; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-top: 15px;">
                <h3 style="color: #2E7D32; margin-top: 0; text-align: center;">🎉 평생금연선언 등록 성공!</h3>
                <p style="font-size: 18px; line-height: 1.6; color: #1B5E20; text-align: center;">
                    <b>정말 칭찬합니다! 아주 훌륭합니다!</b> 👏<br/>
                    {class_id[0]}학년 {class_id[2]}반 친구의 건강하고 깨끗한 약속이 성공적으로 이행되어 보건실 상황판에 수집되었습니다.<br/>
                    앞으로도 유혹에 단호히 맞서며 깨끗한 공기를 만드는 사랑스러운 어린이가 되길 늘 지지하겠습니다!
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
                st.session_state.quiz_step = 1
                st.session_state.quiz_finished = False
                st.rerun()
        else:
            st.markdown("""
            <div class="popup-box">
                🚨 오타가 있거나 띄어쓰기가 틀린 부분이 있습니다! 맨 뒤의 마침표(!)까지 하나하나 똑같아야 다짐이 최종 승인 처리됩니다. 글자를 다시 점검해서 적어주세요.
            </div>
            """, unsafe_allow_html=True)

# ── 🛠️ [보건교사 전용 관리자 대시보드] ───────────────────────────────────────
st.write("")
st.divider()
with st.expander("🔐 보건교사 전용 관리자 대시보드"):
    admin_password = st.text_input("보건교사 암호를 입력하세요:", type="password", key="admin_pwd_main")
    if admin_password == "admin":
        st.markdown("### 🛠️ 보건실 캠페인 통계 제어 센터")
        st.write("학급별 잘못 입력된 데이터(참여 인원)를 개별 수정하거나 전체 데이터를 한 번에 리셋할 수 있습니다.")
        
        # 1. 개별 학급 데이터 수정
        st.markdown("#### 📝 학급별 참여 인원 즉각 수정")
        cls_to_edit = st.selectbox("수정할 학급을 선택하세요:", list(CAPACITIES.keys()), key="admin_cls_select")
        current_val = stats.get(cls_to_edit, 0)
        max_val = CAPACITIES[cls_to_edit]
        
        # 슬라이더 혹은 숫자 입력을 통한 정밀 제어
        new_val = st.number_input(
            f"{cls_to_edit[0]}학년 {cls_to_edit[2]}반 현재 수치 수정 (정원: {max_val}명)", 
            min_value=0, max_value=max_val, value=current_val, step=1, key="admin_num_input"
        )
        
        if st.button("학급 데이터 강제 덮어쓰기 💾", key="admin_save_btn"):
            stats[cls_to_edit] = new_val
            save_stats(stats)
            st.success(f"🎉 성공적으로 {cls_to_edit[0]}학년 {cls_to_edit[2]}반 완료 인원이 {new_val}명으로 수정되었습니다.")
            st.rerun()
            
        st.write("")
        st.divider()
        
        # 2. 전체 데이터 초기화
        st.markdown("#### 🚨 전체 통계 데이터 완전 초기화")
        st.warning("경고: 초기화 버튼을 클릭하면 모든 학급의 하트 완료 데이터가 즉시 [0명]으로 초기화되며 원래대로 복구할 수 없습니다.")
        
        # 실수 방지용 이중 체크박스
        confirm_reset = st.checkbox("데이터 전체 삭제에 동의합니다.", value=False, key="admin_confirm_reset")
        if st.button("🔴 전체 학급 통계 리셋 실행", key="admin_reset_btn", disabled=not confirm_reset):
            reset_data = {k: 0 for k in CAPACITIES.keys()}
            save_stats(reset_data)
            st.success("포항동부초등학교 학급 데이터가 완벽하게 [0명]으로 리셋 완료되었습니다.")
            st.rerun()
            
    elif admin_password:
        st.error("❌ 비밀번호가 올바르지 않습니다. 보건 교사 암호를 정확히 입력해주세요.")
