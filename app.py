from shiny.express import ui, input, render
from shinywidgets import render_plotly
import plotly.express as px
import pathlib
import pandas as pd
from plotly import graph_objects as go

# 데이터 로드
from shared import df_info, df_compare, df_infra_summary, df_bar_long, df_infra_combined, df_stats, df_infra_merged

# ✅ HTML 파일 매핑
축제_파일_매핑 = {
    "작약꽃축제": "작약꽃축제.html",
    "와인페스타": "와인페스타.html",
    "별빛축제": "별빛축제.html",
    "벚꽃축제": "벚꽃축제.html",
    "오미자축제": "오미자축제.html",
    "우주항공축제": "우주항공축제_.html"
}


# ✅ 표 1: 축제 기본정보 (작약꽃축제 통합 버전)
df_info["일일 평균 방문객"] = (df_info["총방문객(명)"] / df_info["일수(일)"]).round(0)
df_info_fixed = df_info.copy()
df_info_fixed.loc[df_info_fixed["축제명"].isin(["작약꽃축제A", "작약꽃축제B", "작약꽃축제C"]), "축제명"] = "작약꽃축제(A/B/C)"
df_info_display = df_info_fixed.drop_duplicates(subset="축제명")[
    ["축제명", "지역", "일수(일)", "총방문객(명)", "일일 평균 방문객", "개최시기(월)"]
].reset_index(drop=True)


# ✅ Overview 탭 UI 구성
ui.page_opts(title="영천시 축제 대시보드", fillable=False)


with ui.nav_panel("Overview"):
    # ▶ 위쪽: 표 1, 2
    with ui.layout_columns(col_widths=(6, 6)):
        with ui.card(style="box-shadow: 2px 2px 8px rgba(0,0,0,0.1); border-radius: 10px;"):
            ui.h4("1. 영천 축제, 왜 이 축제와 비교할까?", style="background-color: #ffe4e6; color: #c2185b; padding: 0.5rem 1rem; border-radius: 6px;")
            @render.ui
            def compare_custom():
                return ui.HTML("""
                <div style="display: flex; flex-direction: column; gap: 2rem; font-family: sans-serif; font-size: 14px;">

                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="flex: 1; background: #f2f2f2; padding: 1rem; border-radius: 10px;">
                            <strong>작약꽃축제</strong><br>
                            일일 평균 방문객: 7,143명
                        </div>
                        <div style="font-size: 20px; color: #999;">→</div>
                        <div style="flex: 1; background: #e6f4ea; padding: 1rem; border-radius: 10px; border-left: 4px solid #67c587;">
                            <strong>🌿 자연 경관(봄꽃) 테마</strong><br>
                            자연을 무대로 한 계절성 축제로 경관 감상 중심으로 구성
                        </div>
                        <div style="font-size: 20px; color: #999;">→</div>
                        <div style="flex: 1; background: #f2f2f2; padding: 1rem; border-radius: 10px;">
                            <strong>옥정호 벚꽃축제</strong><br>
                            일일 평균 방문객: 17,500명
                        </div>
                    </div>

                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="flex: 1; background: #f2f2f2; padding: 1rem; border-radius: 10px;">
                            <strong>별빛축제</strong><br>
                            일일 평균 방문객: 20,000명
                        </div>
                        <div style="font-size: 20px; color: #999;">→</div>
                        <div style="flex: 1; background: #eee5f9; padding: 1rem; border-radius: 10px; border-left: 4px solid #9b6dcc;">
                            <strong>🔬 과학·우주 테마</strong><br>
                              과학관 등 특화 시설과 연계하여 운영되는 테마형 축제
                        </div>
                        <div style="font-size: 20px; color: #999;">→</div>
                        <div style="flex: 1; background: #f2f2f2; padding: 1rem; border-radius: 10px;">
                            <strong>우주항공축제</strong><br>
                            일일 평균 방문객: 30,000명
                        </div>
                    </div>

                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="flex: 1; background: #f2f2f2; padding: 1rem; border-radius: 10px;">
                            <strong>와인페스타</strong><br>
                            일일 평균 방문객: 20,000명
                        </div>
                        <div style="font-size: 20px; color: #999;">→</div>
                        <div style="flex: 1; background: #fff5dd; padding: 1rem; border-radius: 10px; border-left: 4px solid #d4a42c;">
                            <strong>🍇 특산물·과일 테마</strong><br>
                            지역 농산물과 과일 홍보 및 체험 중심의 축제
                        </div>
                        <div style="font-size: 20px; color: #999;">→</div>
                        <div style="flex: 1; background: #f2f2f2; padding: 1rem; border-radius: 10px;">
                            <strong>오미자축제</strong><br>
                            일일 평균 방문객: 16,667명
                        </div>
                    </div>

                </div>
                """)
            
        with ui.card():
            ui.h4("2. 축제별 규모와 개최 정보 한눈에 보기", style="background-color: #fff3e0; color: #ef6c00; padding: 0.5rem 1rem; border-radius: 8px;")
            @render.data_frame
            def info_table():
                return df_info_display
           
            

    # ▶ 아래쪽: 표 3, 그래프 4
    with ui.layout_columns(col_widths=(6, 6)):
        with ui.card():
            ui.h4("3. 축제별 숙소·식당·주차장 인프라 현황", style="background-color: #e0f7fa; color: #00796b; padding: 0.5rem 1rem; border-radius: 6px;")
            @render.data_frame
            def infra_table():
                return df_infra_summary
            
        with ui.card():
            ui.h4("3-1. 업소 수 절대 비교: 어떤 축제가 가장 많을까?", style="background-color: #e0f7fa; color: #00796b; padding: 0.5rem 1rem; border-radius: 6px;")
            ui.input_radio_buttons(
                id="infra_type",
                label="업소 유형 선택",
                choices=["숙소", "식당"],
                selected="숙소",
                inline=True
            )
            # 와인페스타 포함 여부 체크박스
            ui.input_checkbox(
                id='include_wine',
                label = "와인페스타 포함 여부",
                value = True
            )

            @render_plotly
            def infra_bar():
                df_filtered = df_bar_long[df_bar_long["업소유형"] == input.infra_type()]

                # 와인 페스타 필터링
                if not input.include_wine() :
                    df_filtered = df_filtered[df_filtered["축제명"] != "와인페스타"]

                fig = px.bar(
                    df_filtered,
                    x="축제명",
                    y="업소수",
                    color="축제명",
                    title=f"{input.infra_type()} 수 비교",
                    labels={"업소수": f"{input.infra_type()} 수"},
                    height=300
                )
                fig.update_layout(showlegend=False)
                return fig
            
    with ui.card():
        ui.h4("📌 축제 장소 특성 및 인프라 수용력 요약")
        @render.ui
        def festival_locations():
            return ui.HTML("""
                <div style="display: flex; flex-direction: column; gap: 1.5rem; font-size: 14px; font-family: sans-serif;">

                    <div style="background: #f9f9f9; border-left: 5px solid #6da1ff; padding: 1rem; border-radius: 8px;">
                        <strong>작약꽃축제</strong> – 영천 화북면 고지대에 위치, 경관은 뛰어나나 교통·주차 인프라 부족
                    </div>

                    <div style="background: #f9f9f9; border-left: 5px solid #c49fff; padding: 1rem; border-radius: 8px;">
                        <strong>별빛축제</strong> – 천문대 연계 고지대 축제, 숙박 부족 / 야간 행사로 교통 대응 필요
                    </div>

                    <div style="background: #f9f9f9; border-left: 5px solid #8ae2aa; padding: 1rem; border-radius: 8px;">
                        <strong>와인페스타</strong> – 영천 도심 공원 중심, 숙소·음식점 인프라 풍부, 수용력 우수
                    </div>

                    <div style="background: #f9f9f9; border-left: 5px solid #f4b76a; padding: 1rem; border-radius: 8px;">
                        <strong>오미자축제</strong> – 문경 농촌 체험형, 소규모 수용력으로도 운영 무리 없음
                    </div>

                    <div style="background: #f9f9f9; border-left: 5px solid #f293a6; padding: 1rem; border-radius: 8px;">
                        <strong>우주항공축제</strong> – 나로우주센터 중심, 주요 생활권에서 떨어진 지역이나 적정 수준의 인프라 갖춤
                    </div>

                    <div style="background: #f9f9f9; border-left: 5px solid #b1dbff; padding: 1rem; border-radius: 8px;">
                        <strong>옥정호 벚꽃축제</strong> – 수변 경관 중심, 적정 수준의 인프라 갖춤
                    </div>
                </div>
            """)



with ui.nav_panel("Map View"):
    ui.p("좌우 지도를 통해 서로 다른 축제를 선택하고 인프라(숙소, 식당, 카페 등)를 비교", style="font-size: 16px; color: #555;")
    with ui.layout_columns(col_widths=(6, 6)):
        with ui.card():
            ui.h4("📍 왼쪽 지도 (선택한 축제 위치)")
            ui.input_select("left_festival", "🎯 왼쪽 지도: 축제를 선택하세요", list(축제_파일_매핑.keys()), selected="작약꽃축제")
            @render.ui
            def map_left():
                filename = 축제_파일_매핑[input.left_festival()]
                return ui.HTML(f'<iframe src="{filename}" width="100%" height="600px" style="border:none;"></iframe>')

        with ui.card():
            ui.h4("📍 오른쪽 지도 (선택한 축제 위치)")
            ui.input_select("right_festival", "🎯 오른쪽 지도: 축제를 선택하세요", list(축제_파일_매핑.keys()), selected="와인페스타")
            @render.ui
            def map_right():
                filename = 축제_파일_매핑[input.right_festival()]
                return ui.HTML(f'<iframe src="{filename}" width="100%" height="600px" style="border:none;"></iframe>')


with ui.nav_panel("Stats View"):
    # ✅ 데이터 로딩
    축제_목록 = sorted(df_stats["축제명"].dropna().unique().tolist())
    숙소_세부 = sorted(df_stats[df_stats["구분1"] == "숙소"]["구분2"].dropna().unique().tolist())
    식당_세부 = sorted(df_stats[df_stats["구분1"] == "식당"]["구분2"].dropna().unique().tolist())

    # ✅ 사이드바 및 본문 레이아웃
    with ui.layout_sidebar():
        with ui.sidebar(title="Filter controls", open="desktop", bg="#f8f8f8"):
            ui.input_select(
                id="selected_festival",
                label="🎯 축제를 선택하세요",
                choices=축제_목록,
                selected=축제_목록[0],
                multiple=False,
                width="100%"
            )
            ui.input_checkbox_group(
                id="숙소세부",
                label="🏨 숙소 유형 필터",
                choices=숙소_세부,
                selected=숙소_세부
            )
            ui.input_checkbox_group(
                id="식당세부",
                label="🍽️ 식당 유형 필터",
                choices=식당_세부,
                selected=식당_세부
            )

        # ✅ 📊 그래프 3개 깔끔하게 정렬
        with ui.layout_columns(col_widths=(6, 6)):
            with ui.card():
                ui.h4("🏨 숙소 유형 분포")
                @render_plotly
                def 숙소차트():
                    df = df_stats[
                        (df_stats["축제명"] == input.selected_festival()) &
                        (df_stats["구분1"] == "숙소") &
                        (df_stats["구분2"].isin(input.숙소세부()))
                    ]
                    count = df["구분2"].value_counts().reset_index()
                    count.columns = ["구분2", "수"]
                    
                    fig =px.pie(
                        count if not count.empty else pd.DataFrame({'구분2' : ["없음"], "수" : [1]}),
                        names = "구분2",
                        values = "수",
                        title="어떤 유형의 숙소가 더 많을까?",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig.update_traces(textinfo = "percent+label", textposition = 'outside', textfont_size = 15)
                    return fig
                
            with ui.card():
                ui.h4("🍽️ 식당 종류 분포")
                @render_plotly
                def 식당차트():
                    df = df_stats[
                        (df_stats["축제명"] == input.selected_festival()) &
                        (df_stats["구분1"] == "식당") &
                        (df_stats["구분2"].isin(input.식당세부()))
                    ]
                    count = df["구분2"].value_counts().reset_index()
                    count.columns = ["구분2", "수"]
                    
                    selected = input.selected_festival()
                    text_size = 13 if selected == "와인페스타" else 15

                    fig = px.pie(
                        count if not count.empty else pd.DataFrame({"구분2":["없음"], "수":[1]}),
                        names = "구분2",
                        values = "수",
                        title="어떤 종류의 식당이 더 많을까?",
                        hole = 0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig.update_traces(textinfo = "percent+label", textposition = 'outside', textfont_size = text_size)
                    return fig


        with ui.layout_columns(col_widths=(6, 6)):
            # 카페 차트는 제거됨
            with ui.card():
                ui.h4("🅿️ 공영주차장 수")
                @render_plotly
                def 주차장차트():
                    # ✅ 주차장 데이터 필터링
                    df_주차 = df_stats[df_stats["구분1"] == "주차장"].copy()
                
                    # ✅ 전체 축제명과 구분2 목록 추출
                    축제_목록 = df_stats["축제명"].dropna().unique()
                    구분2_목록 = df_주차["구분2"].dropna().unique()
                
                    # ✅ 모든 축제 × 구분2 조합 생성
                    전체_조합 = pd.MultiIndex.from_product(
                        [축제_목록, 구분2_목록],
                        names=["축제명", "구분2"]
                    ).to_frame(index=False)
                
                    # ✅ 실제 데이터 집계
                    count = df_주차.groupby(["축제명", "구분2"]).size().reset_index(name="수")
                
                    # ✅ 누락된 조합에 대해 수 = 0 으로 채움
                    merged = pd.merge(전체_조합, count, on=["축제명", "구분2"], how="left").fillna(0)
                    merged["수"] = merged["수"].astype(int)
                
                    selected = input.selected_festival()
                
                    # ✅ 그래프 생성: 막대 위에 값 표시
                    fig = px.bar(
                        merged,
                        x="구분2",
                        y="수",
                        color="축제명",
                        barmode="group",
                        text="수",  # 막대 위 숫자 표시
                        title="공영주차장 수 - 전체 축제 비교(축제위치 반경 1km이내 기준)",
                        labels={"구분2": "주차장 유형", "수": "개수"},
                        height=450,
                        color_discrete_sequence = px.colors.qualitative.Pastel
                    )
                
                    # ✅ 각 막대 위에 수치 표시 & 선택된 축제 강조
                    for trace in fig.data:
                        trace.textposition = "outside"
                        trace.marker.opacity = 1.0 if trace.name == selected else 0.2
                
                    # ✅ x축 라벨 잘 보이게 설정
                    fig.update_layout(
                        legend_title_text="축제명",
                        showlegend=True,
                        yaxis=dict(tick0=0, dtick=10),
                        xaxis=dict(
                            tickangle=0,
                            automargin=True,
                            tickfont=dict(size=12),
                            title="주차장 유형"
                        ),
                        margin=dict(b=80)  # 하단 여백 확보
                    )
                
                    return fig
                
                # ▶ 셔틀버스 운행 정보 표 (HTML 버전)
        with ui.layout_columns(col_widths=(12,)):
            with ui.card(full_screen=True):
                ui.h4("🚌축제 셔틀버스 운행 정보")
        
                @render.ui
                def shuttle_table():
                    return ui.HTML("""
                    <style>
                        table.shuttle-table {
                            width: 100%;
                            border-collapse: collapse;
                            font-size: 14px;
                        }
                        table.shuttle-table th, table.shuttle-table td {
                            border: 1px solid #ddd;
                            padding: 8px;
                            text-align: center;
                        }
                        table.shuttle-table th {
                            background-color: #f2f2f2;
                        }
                    </style>
        
                    <table class="shuttle-table">
                        <thead>
                            <tr>
                                <th>축제명</th>
                                <th>운행 유무</th>
                                <th>경로</th>
                                <th>운행 횟수</th>
                                <th>운영 시간</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>영천 작약꽃축제</td>
                                <td>있음</td>
                                <td>버스터미널 → 영천역 → 영천시청 → 영천한의마을 등 순환</td>
                                <td>약 15분 간격</td>
                                <td>11:00 ~ 22:00</td>
                            </tr>
                            <tr>
                                <td>별빛축제</td>
                                <td>있음</td>
                                <td>이천터미널 → 별빛정원우주</td>
                                <td>1시간 간격</td>
                                <td>16:30 ~ 19:30</td>
                            </tr>
                            <tr>
                                <td>와인페스타</td>
                                <td>있음</td>
                                <td>제1주차장 앞 ↔ 행사장</td>
                                <td>수시 운행</td>
                                <td>행사 시간에 맞춰 운행</td>
                            </tr>
                            <tr>
                                <td>고흥항공우주축제</td>
                                <td>있음</td>
                                <td>신금리 ↔ 우주과학관</td>
                                <td>2대 순환 운행</td>
                                <td>09:00 ~ 21:00</td>
                            </tr>
                            <tr>
                                <td>옥정호 벚꽃축제</td>
                                <td>있음</td>
                                <td>쌍암리 주차장(운암초 근처) ↔ 축제 행사장</td>
                                <td>수시 운행</td>
                                <td>09:00 ~ 18:00</td>
                            </tr>
                            <tr>
                                <td>문경 오미자축제</td>
                                <td>있음</td>
                                <td>문경오미자테마공원 ↔ 문경새재 2주차장</td>
                                <td>수시 운행</td>
                                <td>10:00 ~ 18:00</td>
                            </tr>
                        </tbody>
                    </table>
                    """)
                    
        with ui.layout_columns(col_widths=(6,6)):
            with ui.card():
                ui.h4("🎯 인프라 수 vs 일일 방문객 수 비교")
                df_bar_long["축제명"] = df_bar_long["축제명"].replace({
                    "작약꽃축제A": "작약꽃축제(A/B/C)",
                    "작약꽃축제B": "작약꽃축제(A/B/C)",
                    "작약꽃축제C": "작약꽃축제(A/B/C)"})
                
                df_info["축제명"] = df_info["축제명"].replace({
                    "작약꽃축제A": "작약꽃축제(A/B/C)",
                    "작약꽃축제B": "작약꽃축제(A/B/C)",    
                    "작약꽃축제C": "작약꽃축제(A/B/C)"})

                # 필터: 영천 축제 선택 + 업소 유형 선택

                축제_비교_목록 = ["작약꽃축제(A/B/C)", "와인페스타", "별빛축제"]
                업소유형목록 = sorted(df_bar_long["업소유형"].unique())

                ui.input_select("비교기준축제", "✔ 영천시 축제를 선택하세요", 축제_비교_목록, selected="작약꽃축제(A/B/C)")
                ui.input_checkbox_group("비교업소유형", "✔ 업소 유형 선택", 업소유형목록, selected=업소유형목록)

                @render_plotly
                def infra_visitor_graph():
                    import plotly.graph_objects as go
                    import plotly.express as px

                    festival_pair = {
                        "작약꽃축제(A/B/C)": ["작약꽃축제(A/B/C)", "옥정호 벚꽃축제"],
                        "와인페스타": ["와인페스타", "오미자축제"],
                        "별빛축제": ["별빛축제", "우주항공축제"]
                    }

                    선택축제 = input.비교기준축제()
                    선택업소유형 = input.비교업소유형()
                    비교축제들 = festival_pair[선택축제]

                    df_filtered = df_bar_long[
                        (df_bar_long["축제명"].isin(비교축제들)) &
                        (df_bar_long["업소유형"].isin(선택업소유형))
                    ]

                    fig = go.Figure()
                    color_list = px.colors.qualitative.Pastel

                    # ✅ 막대그래프 (왼쪽 y축)
                    for i, 유형 in enumerate(선택업소유형):
                        df_sub = df_filtered[df_filtered["업소유형"] == 유형]
                        fig.add_trace(go.Bar(
                            x=df_sub["축제명"],
                            y=df_sub["업소수"],
                            name=유형,
                            marker_color=color_list[i % len(color_list)],
                            yaxis="y"  # 기본값이라 생략 가능
                        ))

                    # ✅ 방문객 수 점 그래프 (오른쪽 y축)
                    visitor_dict = df_info.set_index("축제명")["일일방문객(명)"].to_dict()
                    visitor_raw = [visitor_dict.get(f, 0) for f in 비교축제들]

                    fig.add_trace(go.Scatter(
                        x=비교축제들,
                        y=visitor_raw,
                        mode="markers+text",
                        name="일일 방문객 수",
                        text=[f"{v:,.0f}명" for v in visitor_raw],
                        textposition="top center",
                        marker=dict(size=12, color="black", symbol="diamond"),
                        yaxis="y2"
                    ))
        
                    # ✅ 이중 y축 설정
                    fig.update_layout(
                        barmode="stack",
                        title=f"{선택축제} vs 유사 축제: 인프라 + 방문객 수 비교",
                        xaxis_title="축제명",
                        yaxis=dict(
                            title="숙소/식당 수",
                            side="left"
                        ),
                        yaxis2=dict(
                            title="일일 방문객 수 (명)",
                            overlaying="y",
                            side="right",
                            range=[0, 40000],
                            showgrid=False
                        ),
                        legend_title="항목",
                        height=550
                    )
        
                    return fig
        


with ui.nav_panel("Insight View"):
    "💡 인사이트 도출 페이지입니다."