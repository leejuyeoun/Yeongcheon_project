from shiny.express import ui, input, render
from shinywidgets import render_plotly
import plotly.express as px
import pathlib
import pandas as pd
from plotly import graph_objects as go
from shiny import reactive

from shinyswatch import theme
ui.page_opts(title="영천시 축제 대시보드", theme=theme.lux, fillable=False)

# 데이터 로드
from shared import df_info, df_compare, df_infra_summary, df_bar_long, df_infra_combined, df_stats, df_infra_merged

# ✅ HTML 파일 매핑
축제_파일_매핑 = {
    "작약꽃축제": "작약꽃축제_.html",
    "와인페스타": "와인페스타_.html",
    "별빛축제": "별빛축제_.html",
    "벚꽃축제": "벚꽃축제_.html",
    "오미자축제": "오미자축제_.html",
    "우주항공축제": "우주항공축제.html"
}


# ✅ 표 1: 축제 기본정보 (작약꽃축제 통합 버전)
df_info["일일 평균 방문객"] = (df_info["총방문객(명)"] / df_info["일수(일)"]).round(0)
df_info_fixed = df_info.copy()
df_info_fixed.loc[df_info_fixed["축제명"].isin(["작약꽃축제A", "작약꽃축제B", "작약꽃축제C"]), "축제명"] = "작약꽃축제(A/B/C)"
df_info_display = df_info_fixed.drop_duplicates(subset="축제명")[
    ["축제명", "지역", "일수(일)", "총방문객(명)", "일일 평균 방문객", "개최시기(월)"]
].reset_index(drop=True)


with ui.nav_panel("Festival Snapshot"):
    ui.h2(" 축제 한눈에 보기", style="margin-bottom: 2rem;")

# ▶ Festival Snapshot 패널 안 CSS 정의 부분에서 다음 내용 추가

    ui.HTML("""
    <style>
        .hover-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .hover-card:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            cursor: pointer;
        }

        /* ✅ 수정된 부분: hover-button 스타일 정의 */
        .hover-button {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .hover-button:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
            cursor: pointer;
            background-color: #4d6d91 !important;
        }
    </style>

    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const cards = document.querySelectorAll(".hover-card");
            const festivalValues = ["작약꽃축제A", "와인페스타", "별빛축제"];

            cards.forEach(function(card, index) {
                card.addEventListener("click", function() {
                    Shiny.setInputValue("__nav_festival_snapshot__", "Stats View", {priority: "event"});
                    setTimeout(function () {
                        const dropdown = document.querySelector('select#selected_festival');
                        if (dropdown) {
                            dropdown.value = festivalValues[index];
                            dropdown.dispatchEvent(new Event("change", { bubbles: true }));
                        }
                    }, 500);
                });
            });
        });
    </script>
    """)


    with ui.layout_columns(gap="2rem", col_widths=(4, 4, 4)):

        # ✅ 작약꽃축제 카드
        ui.HTML("""
        <div class="festival-card hover-card" style="background-color: #FAFAFA; border: 2px solid #DB6C7E; border-radius: 10px; overflow: hidden; font-family: sans-serif; color: #DB6C7E;">
            <div style="background-color: #DB6C7E; color: white; padding: 0.8rem 1.2rem; font-size: 1.3rem; font-weight: bold;">🌸 작약꽃축제</div>
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 2px solid #DB6C7E;">
                <img src="/peony.jpg" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div style="display: flex; border-bottom: 2px solid #DB6C7E;">
                <div style="flex: 1; display: flex; flex-direction: column; border-right: 2px solid #DB6C7E;">
                    <div style="flex: 2; padding: 1rem; font-weight: bold;">숙소: 32개<br>식당: 80개<br>주차장: 9개<br>화장실: 22개</div>
                    <div style="flex: 1; padding: 0.8rem; border-top: 2px solid #DB6C7E;">한약축제와 연계 / 분산형 개최</div>
                </div>
                <div style="flex: 1; padding: 1rem;">한방·자연 테마 복합 이벤트</div>
            </div>
            <div style="display: flex; border-bottom: 2px solid #DB6C7E;">
                <div style="flex: 1; padding: 1rem; border-right: 2px solid #DB6C7E;">
                    총 방문객 5만 명<br>
                    <span style="color: #DB6C7E; font-size: 1.2rem; font-weight: bold;">1일 방문객 7천 명</span>
                </div>
                <div style="flex: 3; padding: 1rem;">유사축제: 옥정호 벚꽃축제</div>
            </div>
            <div style="padding: 1rem; background-color: #FAFAFA;"><strong>경관 우수하나 교통 및 주차 인프라 부족</strong></div>
        </div>
        """)

        # ✅ 와인페스타 카드
        ui.HTML("""
        <div class="festival-card hover-card" style="background-color: #FAFAFA; border: 2px solid #8d6e63; border-radius: 10px; overflow: hidden; font-family: sans-serif; color: #8d6e63;">
            <div style="background-color: #8d6e63; color: white; padding: 0.8rem 1.2rem; font-size: 1.3rem; font-weight: bold;">🍷 와인페스타</div>
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 2px solid #8d6e63;">
                <img src="/wine.jpg" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div style="display: flex; border-bottom: 2px solid #8d6e63;">
                <div style="flex: 1; display: flex; flex-direction: column; border-right: 2px solid #8d6e63;">
                    <div style="flex: 2; padding: 1rem; font-weight: bold;">숙소: 82개<br>식당: 1,485개<br>주차장: 122개<br>화장실: 158개</div>
                    <div style="flex: 1; padding: 0.8rem; border-top: 2px solid #8d6e63;">한우축제와 연계 / 도심 개최</div>
                </div>
                <div style="flex: 1; padding: 1rem;">도심형 와인 특산물 중심 축제</div>
            </div>
            <div style="display: flex; border-bottom: 2px solid #8d6e63;">
                <div style="flex: 1; padding: 1rem; border-right: 2px solid #8d6e63;">
                    총 방문객 4만 명<br>
                    <span style="color: #8d6e63; font-size: 1.2rem; font-weight: bold;">1일 방문객 2만 명</span>
                </div>
                <div style="flex: 3; padding: 1rem;">유사축제: 문경 오미자축제</div>
            </div>
            <div style="padding: 1rem; background-color: #FAFAFA;"><strong>도심 기반으로 수용력 및 접근성 우수</strong></div>
        </div>
        """)

        # ✅ 별빛축제 카드
        ui.HTML("""
        <div class="festival-card hover-card" style="background-color: #FAFAFA; border: 2px solid #745D8E; border-radius: 10px; overflow: hidden; font-family: sans-serif; color: #745D8E;">
            <div style="background-color: #745D8E; color: white; padding: 0.8rem 1.2rem; font-size: 1.3rem; font-weight: bold;">🌌 별빛축제</div>
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 2px solid #745D8E;">
                <img src="/starlight.jpg" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div style="display: flex; border-bottom: 2px solid #745D8E;">
                <div style="flex: 1; display: flex; flex-direction: column; border-right: 2px solid #745D8E;">
                    <div style="flex: 2; padding: 1rem; font-weight: bold;">숙소: 24개<br>식당: 25개<br>주차장: 6개<br>화장실: 16개</div>
                    <div style="flex: 1; padding: 0.8rem; border-top: 2px solid #745D8E;">보현산 정상 개최 / 캠핑장 연계</div>
                </div>
                <div style="flex: 1; padding: 1rem;">천문대 연계 야간 체험형 축제</div>
            </div>
            <div style="display: flex; border-bottom: 2px solid #745D8E;">
                <div style="flex: 1; padding: 1rem; border-right: 2px solid #745D8E;">
                    총 방문객 6만 명<br>
                    <span style="color: #745D8E; font-size: 1.2rem; font-weight: bold;">1일 방문객 2만 명</span>
                </div>
                <div style="flex: 3; padding: 1rem;">유사축제: 고흥 항공우주축제</div>
            </div>
            <div style="padding: 1rem; background-color: #FAFAFA;"><strong>숙박 부족 및 야간 교통 대응이 과제로 남음</strong></div>
        </div>
        """)






    # ▶ '유사 축제와 비교하기' 버튼 부분 전체 수정본

    with ui.div(style="display: flex; justify-content: center; margin-top: 2rem;"):
        ui.input_action_button(
            "compare_button",
            "유사 축제와 비교하기",
            class_="btn btn-lg",
            style=(
                "width: 100%; max-width: 960px; font-size: 20px; padding: 1.2rem 2rem; "
                "background-color: #5a7dad; color: white; border: none; border-radius: 12px; font-weight: bold;"
            )
        )


    # ▶ JS 코드: 카드 클릭 시 Stats View 이동
    ui.HTML("""
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            document.querySelectorAll(".hover-card").forEach(function(card) {
                card.addEventListener("click", function() {
                    const tab = document.querySelector('a[data-value="Stats View"]');
                    if (tab) tab.click();
                });
            });
        });
    </script>
    """)

    # ▶ JS 코드: 버튼 클릭 시 Map View 이동 및 포커스 해제
    ui.HTML("""
    <script>
        setTimeout(function() {
            const btn = document.getElementById("compare_button");
            if (btn) {
                btn.onclick = function() {
                    const tab = document.querySelector('a[data-value="Map View"]');
                    if (tab) tab.click();
                    btn.blur(); // 포커스 해제
                };
            }
        }, 300);
    </script>
    """)



with ui.nav_panel("Map View"):
    # ✅ 제목 + 버튼을 같은 줄에 배치
    with ui.layout_columns(col_widths=(5, 2, 2, 2)):  # 제목:5, 버튼3개
        ui.h4("유사 축제 인프라 비교", style="margin-top: 1rem; color: #444;")

        ui.input_action_button("btn1", "작약꽃 vs 벚꽃")
        ui.input_action_button("btn2", "와인 vs 오미자")
        ui.input_action_button("btn3", "별빛 vs 우주항공")

        # 🌸 작약꽃 vs 벚꽃
        @reactive.effect
        @reactive.event(input.btn1)
        def _():
            m = ui.modal(
                ui.markdown("""
                <style>
                    table.custom-table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 1em;
                    }
                    .custom-table th, .custom-table td {
                        padding: 10px 15px;
                        text-align: left;
                        vertical-align: top;
                    }
                    .custom-table th {
                        white-space: nowrap;
                    }
                </style>

                <table class="custom-table">
                  <thead>
                    <tr>
                      <th>항목 </th>
                      <th>작약꽃축제 (영천)</th>
                      <th>벚꽃축제 (옥정호)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr><td>시기</td><td>5월 중순</td><td>4월 초</td></tr>
                    <tr><td>장소</td><td>보현산 자락</td><td>옥정호 출렁다리 앞</td></tr>
                    <tr><td>특성</td><td>약초·작약 체험 중심</td><td>수변 경관 감상 중심</td></tr>
                    <tr><td>인프라 </td><td>소규모 숙소, 한약재 음식</td><td>숙소 확충 중, 특산물 먹거리</td></tr>
                    <tr><td>접근성 </td><td>자가용 권장, 주차장 있음</td><td>대중교통 가능, 주차장 있음</td></tr>
                  </tbody>
                </table>
                """),
                    easy_close=True,
                    footer=None,
                    class_="modal-xl"
            )
            ui.modal_show(m)

        # 🍷 와인 vs 오미자
        @reactive.effect
        @reactive.event(input.btn2)
        def _():
            m = ui.modal(
                ui.markdown("""
                <style>
                    table.custom-table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 1em;
                    }
                    .custom-table th, .custom-table td {
                        padding: 10px 15px;
                        text-align: left;
                        vertical-align: top;
                    }
                    .custom-table th {
                        white-space: nowrap;
                    }
                </style>
                
                <table class="custom-table">
                  <thead>
                    <tr>
                      <th>항목</th>
                      <th>와인페스타 (영천)</th>
                      <th>오미자축제 (문경)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr><td>시기</td><td>10월 중순</td><td>9월 중순</td></tr>
                    <tr><td>장소</td><td>영천강변공원</td><td>문경 금천둔치</td></tr>
                    <tr><td>특성</td><td>포도 와인 산업 중심</td><td>전국 최대 오미자 생산지</td></tr>
                    <tr><td>프로그램</td><td>와인 체험·공연</td><td>오미자 체험·공연</td></tr>
                    <tr><td>인프라</td><td>다양한 숙소, 음식점 운영</td><td>숙소·자연휴양림 활용, 향토음식</td></tr>
                  </tbody>
                </table>
                """),
                    easy_close=True,
                    footer=None,
                    class_="modal-xl"
            )
            ui.modal_show(m)

        # 🌌 별빛 vs 우주항공
        @reactive.effect
        @reactive.event(input.btn3)
        def _():
            m = ui.modal(
                ui.markdown("""
                <style>
                    table.custom-table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 1em;
                    }
                    .custom-table th, .custom-table td {
                        padding: 10px 15px;
                        text-align: left;
                        vertical-align: top;
                    }
                    .custom-table th {
                        white-space: nowrap;
                    }
                </style>

                <table class="custom-table">
                  <thead>
                    <tr>
                      <th>항목</th>
                      <th>별빛축제 (영천)</th>
                      <th>우주항공축제 (고흥)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr><td>시기</td><td>10월 초</td><td>5월 초</td></tr>
                    <tr><td>장소</td><td>보현산 천문과학관</td><td>나로우주센터 우주과학관</td></tr>
                    <tr><td>특성</td><td>천문학 체험 중심</td><td>우주항공 산업 체험 중심</td></tr>
                    <tr><td>프로그램</td><td>관측, 강연, 체험</td><td>전시, 우주복 체험 등 다양</td></tr>
                    <tr><td>인프라</td><td>다양한 숙소·먹거리 제공</td><td>숙소·음식 다양, 바지락 활용</td></tr>
                  </tbody>
                </table>
                """),
                    easy_close=True,
                    footer=None,
                    class_="modal-xl"
                )
            ui.modal_show(m)

    ui.p("아래에서 두 개의 축제를 선택하고 위치 및 인프라를 비교하세요.", style="font-size: 15px; color: #666;")


    # 축제 선택 필터
    with ui.layout_columns(col_widths=(6, 6)):
        with ui.card():
            ui.h5("왼쪽 축제 선택", style="color: #333;")
            ui.input_select("left_festival", "왼쪽 지도: 축제를 선택하세요", list(축제_파일_매핑.keys()), selected="작약꽃축제")

        with ui.card():
            ui.h5("오른쪽 축제 선택", style="color: #333;")
            ui.input_select("right_festival", "오른쪽 지도: 축제를 선택하세요", list(축제_파일_매핑.keys()), selected="벚꽃축제")

    # 지도 및 인프라 요약 정보
    with ui.layout_columns(col_widths=(6, 6)):
        with ui.card():
            ui.h5("왼쪽 축제 위치 지도")
            @render.ui
            def map_left():
                filename = 축제_파일_매핑[input.left_festival()]
                return ui.HTML(f'<iframe src="{filename}" width="100%" height="500px" style="border:none; border-radius: 8px;"></iframe>')

            # 왼쪽 축제 인프라 요약 박스
            def infra_summary(festival):
                df = df_infra_merged[df_infra_merged["축제명"].str.contains(festival, na=False)]
                숙소 = df[df["구분1"] == "숙소"].shape[0]
                식당 = df[df["구분1"] == "식당"].shape[0]
                화장실 = df[df["구분1"] == "화장실"].shape[0]
                주차장 = df[df["구분1"] == "주차장"].shape[0]
                return 숙소, 식당, 화장실, 주차장

            with ui.layout_columns(col_widths=[3, 3, 3, 3]):
                with ui.value_box():
                    "숙소 (반경 10km)"
                    @render.express
                    def vb1():
                        f"{infra_summary(input.left_festival())[0]}개"

                with ui.value_box():
                    "식당 (반경 10km)"
                    @render.express
                    def vb2():
                        f"{infra_summary(input.left_festival())[1]}개"

                with ui.value_box():
                    "화장실 (반경 1km)"
                    @render.express
                    def vb3():
                        f"{infra_summary(input.left_festival())[2]}개"

                with ui.value_box():
                    "공영주차장 (반경 1km)"
                    @render.express
                    def vb4():
                        f"{infra_summary(input.left_festival())[3]}개"

        with ui.card():
            ui.h5("오른쪽 축제 위치 지도")
            @render.ui
            def map_right():
                filename = 축제_파일_매핑[input.right_festival()]
                return ui.HTML(f'<iframe src="{filename}" width="100%" height="500px" style="border:none; border-radius: 8px;"></iframe>')

            with ui.layout_columns(col_widths=[3, 3, 3, 3]):
                with ui.value_box():
                    "숙소 (반경 10km)"
                    @render.express
                    def vb5():
                        f"{infra_summary(input.right_festival())[0]}개"

                with ui.value_box():
                    "식당 (반경 10km)"
                    @render.express
                    def vb6():
                        f"{infra_summary(input.right_festival())[1]}개"

                with ui.value_box():
                    "화장실 (반경 1km)"
                    @render.express
                    def vb7():
                        f"{infra_summary(input.right_festival())[2]}개"

                with ui.value_box():
                    "주차장 (반경 1km)"
                    @render.express
                    def vb8():
                        f"{infra_summary(input.right_festival())[3]}개"



    # 세부 유형 막대그래프
    with ui.layout_columns(col_widths=[6, 6]):  # ✅ 카드 너비 균등 조절
        with ui.card():
            ui.h5("왼쪽 축제 인프라 세부 유형")
            @render_plotly
            def bar_left():
                df = df_infra_merged[df_infra_merged["축제명"].str.contains(input.left_festival(), na=False)]
                df = df[df["구분1"].isin(["숙소", "식당"])]
                g = df.groupby(["구분1", "구분2"]).size().reset_index(name="count")

                fig = px.bar(
                    g, x="구분2", y="count", color="구분1",
                    barmode="group",
                    text="count",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    labels={
                        "구분1": "인프라 유형",
                        "구분2": "인프라 세부 유형",
                        "count": "개수"
                    }
                )

                fig.update_traces(textposition="outside", cliponaxis=False)
                fig.update_layout(
                    height=470,
                    margin=dict(l=10, r=10, t=80, b=40),  # 하단 여백도 약간 여유
                    font=dict(size=16),
                    xaxis_tickangle=-30,  # ✅ x축 라벨 겹침 방지
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.1,
                        xanchor="center",
                        x=0.5,
                        title_font=dict(size=16)
                    )
                )
                return fig

        with ui.card():
            ui.h5("오른쪽 축제 인프라 세부 유형")
            @render_plotly
            def bar_right():
                df = df_infra_merged[df_infra_merged["축제명"].str.contains(input.right_festival(), na=False)]
                df = df[df["구분1"].isin(["숙소", "식당"])]
                g = df.groupby(["구분1", "구분2"]).size().reset_index(name="count")

                fig = px.bar(
                    g, x="구분2", y="count", color="구분1",
                    barmode="group",
                    text="count",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    labels={
                        "구분1": "인프라 유형",
                        "구분2": "인프라 세부 유형",
                        "count": "개수"
                    }
                )

                fig.update_traces(textposition="outside", cliponaxis=False)
                fig.update_layout(
                    height=470,
                    margin=dict(l=10, r=10, t=80, b=40),
                    font=dict(size=16),
                    xaxis_tickangle=-30,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.1,
                        xanchor="center",
                        x=0.5,
                        title_font=dict(size=16)
                    )
                )
                return fig

    with ui.card():
        ui.h5("주요 인프라 항목 수 비교", style="margin-top: 1rem;")
        @render_plotly
        def infra_compare_bar():
            left = input.left_festival()
            right = input.right_festival()
            df = df_infra_merged.copy()
            df = df[df["구분1"].isin(["숙소", "식당", "화장실", "주차장"])]

            # 요약 데이터프레임 생성
            summary = df[df["축제명"].str.contains(left, na=False)].groupby("구분1").size().reset_index(name=left)
            summary2 = df[df["축제명"].str.contains(right, na=False)].groupby("구분1").size().reset_index(name=right)
            merged = pd.merge(summary, summary2, on="구분1", how="outer").fillna(0)

            df_plot = pd.melt(merged, id_vars="구분1", var_name="축제명", value_name="개수")

            fig = px.bar(
                df_plot,
                x="구분1",
                y="개수",
                color="축제명",
                barmode="group",
                text="개수",  # ✅ 막대 위 텍스트 표시
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            # ✅ 전체 레이아웃 조정 (폰트 크기 포함)
            fig.update_traces(textposition="outside")
            fig.update_layout(
                height=450,
                xaxis_title="인프라 유형",  # ✅ x축 제목 변경
                font=dict(size=16),       # ✅ 전체 글자 크기 키우기
                legend_title_font=dict(size=16),
                xaxis=dict(tickfont=dict(size=14)),
                yaxis=dict(tickfont=dict(size=14)),
                margin=dict(l=40, r=40, t=40, b=40),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.05,
                    xanchor="center",
                    x=0.5
                )
            )
            return fig











with ui.nav_panel("Stats View"):
    # ✅ 데이터 로딩
    축제_목록 = sorted(df_stats["축제명"].dropna().unique().tolist())
    숙소_세부 = sorted(df_stats[df_stats["구분1"] == "숙소"]["구분2"].dropna().unique().tolist())
    식당_세부 = sorted(df_stats[df_stats["구분1"] == "식당"]["구분2"].dropna().unique().tolist())

    # ✅ 사이드바 및 본문 레이아웃
    with ui.layout_sidebar():
        with ui.sidebar():
            ui.input_select(
                id="selected_festival",
                label="축제를 선택하세요",
                choices=축제_목록,
                selected=축제_목록[0],
                multiple=False,
                width="100%"
            );
            ui.input_checkbox_group(
                id="숙소세부",
                label="숙소 유형 필터",
                choices=숙소_세부,
                selected=숙소_세부
            );
            ui.input_checkbox_group(
                id="식당세부",
                label="식당 유형 필터",
                choices=식당_세부,
                selected=식당_세부
            );

        # ✅ 📊 그래프 3개 깔끔하게 정렬
        with ui.layout_columns(col_widths=(6, 6)):
            with ui.card():
                ui.h4("숙소 유형 분포")
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
                    );
                    fig.update_traces(textinfo = "percent+label", textposition = 'outside', textfont_size = 15);
                    return fig
                
            with ui.card():
                ui.h4("식당 종류 분포")
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
                    );
                    fig.update_traces(textinfo = "percent+label", textposition = 'outside', textfont_size = text_size);
                    return fig


        # with ui.layout_columns(col_widths=(6, 6)):
        #     # 카페 차트는 제거됨
        #     with ui.card():
        #         ui.h4("공영주차장 수")
        #         @render_plotly
        #         def 주차장차트():
        #             # ✅ 주차장 데이터 필터링
        #             df_주차 = df_stats[df_stats["구분1"] == "주차장"].copy()
                
        #             # ✅ 전체 축제명과 구분2 목록 추출
        #             축제_목록 = df_stats["축제명"].dropna().unique()
        #             구분2_목록 = df_주차["구분2"].dropna().unique()
                
        #             # ✅ 모든 축제 × 구분2 조합 생성
        #             전체_조합 = pd.MultiIndex.from_product(
        #                 [축제_목록, 구분2_목록],
        #                 names=["축제명", "구분2"]
        #             ).to_frame(index=False)
                
        #             # ✅ 실제 데이터 집계
        #             count = df_주차.groupby(["축제명", "구분2"]).size().reset_index(name="수")
                
        #             # ✅ 누락된 조합에 대해 수 = 0 으로 채움
        #             merged = pd.merge(전체_조합, count, on=["축제명", "구분2"], how="left").fillna(0)
        #             merged["수"] = merged["수"].astype(int)
                
        #             selected = input.selected_festival()
                
        #             # ✅ 그래프 생성: 막대 위에 값 표시
        #             fig = px.bar(
        #                 merged,
        #                 x="구분2",
        #                 y="수",
        #                 color="축제명",
        #                 barmode="group",
        #                 text="수",  # 막대 위 숫자 표시
        #                 title="공영주차장 수 - 전체 축제 비교(축제위치 반경 1km이내 기준)",
        #                 labels={"구분2": "주차장 유형", "수": "개수"},
        #                 height=450,
        #                 color_discrete_sequence = px.colors.qualitative.Pastel
        #             );
                
        #             # ✅ 각 막대 위에 수치 표시 & 선택된 축제 강조
        #             for trace in fig.data:
        #                 trace.textposition = "outside"
        #                 trace.marker.opacity = 1.0 if trace.name == selected else 0.2
                
        #             # ✅ x축 라벨 잘 보이게 설정
        #             fig.update_layout(
        #                 legend_title_text="축제명",
        #                 showlegend=True,
        #                 yaxis=dict(tick0=0, dtick=10),
        #                 xaxis=dict(
        #                     tickangle=0,
        #                     automargin=True,
        #                     tickfont=dict(size=12),
        #                     title="주차장 유형"
        #                 ),
        #                 margin=dict(b=80)  # 하단 여백 확보
        #             )
                
        #             return fig
                
        with ui.layout_columns(col_widths=(6, 6)):
            # ✅ 왼쪽: 공중화장실 수 그래프
            with ui.card():
                ui.h4("공중화장실 수")
                @render_plotly
                def 화장실차트():
                    df_화장실 = df_stats[df_stats["구분1"] == "화장실"].copy()
                    축제_목록 = df_stats["축제명"].dropna().unique()
                    구분2_목록 = df_화장실["구분2"].dropna().unique()

                    전체_조합 = pd.MultiIndex.from_product(
                        [축제_목록, 구분2_목록],
                        names=["축제명", "구분2"]
                    ).to_frame(index=False)

                    count = df_화장실.groupby(["축제명", "구분2"]).size().reset_index(name="수")
                    merged = pd.merge(전체_조합, count, on=["축제명", "구분2"], how="left").fillna(0)
                    merged["수"] = merged["수"].astype(int)

                    selected = input.selected_festival()

                    fig = px.bar(
                        merged,
                        x="구분2",
                        y="수",
                        color="축제명",
                        barmode="group",
                        text="수",
                        title="공중화장실 수 - 전체 축제 비교(축제위치 반경 1km이내 기준)",
                        labels={"구분2": "화장실 유형", "수": "개수"},
                        height=450,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )

                    for trace in fig.data:
                        trace.textposition = "outside"
                        trace.marker.opacity = 1.0 if trace.name == selected else 0.2

                    fig.update_layout(
                        legend_title_text="축제명",
                        showlegend=True,
                        yaxis=dict(tick0=0, dtick=10),
                        xaxis=dict(
                            tickangle=0,
                            automargin=True,
                            tickfont=dict(size=12),
                            title="화장실 유형"
                        ),
                        margin=dict(b=80)
                    )

                    return fig

            # ✅ 오른쪽: 공영주차장 수 그래프 (기존 코드 그대로)
            with ui.card():
                ui.h4("공영주차장 수")
                @render_plotly
                def 주차장차트():
                    df_주차 = df_stats[df_stats["구분1"] == "주차장"].copy()
                    축제_목록 = df_stats["축제명"].dropna().unique()
                    구분2_목록 = df_주차["구분2"].dropna().unique()

                    전체_조합 = pd.MultiIndex.from_product(
                        [축제_목록, 구분2_목록],
                        names=["축제명", "구분2"]
                    ).to_frame(index=False)

                    count = df_주차.groupby(["축제명", "구분2"]).size().reset_index(name="수")
                    merged = pd.merge(전체_조합, count, on=["축제명", "구분2"], how="left").fillna(0)
                    merged["수"] = merged["수"].astype(int)

                    selected = input.selected_festival()

                    fig = px.bar(
                        merged,
                        x="구분2",
                        y="수",
                        color="축제명",
                        barmode="group",
                        text="수",
                        title="공영주차장 수 - 전체 축제 비교(축제위치 반경 1km이내 기준)",
                        labels={"구분2": "주차장 유형", "수": "개수"},
                        height=450,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )

                    for trace in fig.data:
                        trace.textposition = "outside"
                        trace.marker.opacity = 1.0 if trace.name == selected else 0.2

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
                        margin=dict(b=80)
                    )

                    return fig








                # ▶ 셔틀버스 운행 정보 표 (HTML 버전)
        with ui.layout_columns(col_widths=(12,)):
            with ui.card(full_screen=True):
                ui.h4("축제 셔틀버스 운행 정보")
        
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
                    
        # with ui.layout_columns(col_widths=(6,6)):
        #     with ui.card():
        #         ui.h4("인프라 수 vs 일일 방문객 수 비교")
        #         df_bar_long["축제명"] = df_bar_long["축제명"].replace({
        #             "작약꽃축제A": "작약꽃축제(A/B/C)",
        #             "작약꽃축제B": "작약꽃축제(A/B/C)",
        #             "작약꽃축제C": "작약꽃축제(A/B/C)"})
                
        #         df_info["축제명"] = df_info["축제명"].replace({
        #             "작약꽃축제A": "작약꽃축제(A/B/C)",
        #             "작약꽃축제B": "작약꽃축제(A/B/C)",    
        #             "작약꽃축제C": "작약꽃축제(A/B/C)"})

        #         # 필터: 영천 축제 선택 + 업소 유형 선택

        #         축제_비교_목록 = ["작약꽃축제(A/B/C)", "와인페스타", "별빛축제"]
        #         업소유형목록 = sorted(df_bar_long["업소유형"].unique())

        #         ui.input_select("비교기준축제", "✔ 영천시 축제를 선택하세요", 축제_비교_목록, selected="작약꽃축제(A/B/C)")
        #         ui.input_checkbox_group("비교업소유형", "✔ 업소 유형 선택", 업소유형목록, selected=업소유형목록)

        #         @render_plotly
        #         def infra_visitor_graph():
        #             import plotly.graph_objects as go
        #             import plotly.express as px

        #             festival_pair = {
        #                 "작약꽃축제(A/B/C)": ["작약꽃축제(A/B/C)", "옥정호 벚꽃축제"],
        #                 "와인페스타": ["와인페스타", "오미자축제"],
        #                 "별빛축제": ["별빛축제", "우주항공축제"]
        #             }

        #             선택축제 = input.비교기준축제()
        #             선택업소유형 = input.비교업소유형()
        #             비교축제들 = festival_pair[선택축제]

        #             df_filtered = df_bar_long[
        #                 (df_bar_long["축제명"].isin(비교축제들)) &
        #                 (df_bar_long["업소유형"].isin(선택업소유형))
        #             ]

        #             fig = go.Figure()
        #             color_list = px.colors.qualitative.Pastel

        #             # ✅ 막대그래프 (왼쪽 y축)
        #             for i, 유형 in enumerate(선택업소유형):
        #                 df_sub = df_filtered[df_filtered["업소유형"] == 유형]
        #                 fig.add_trace(go.Bar(
        #                     x=df_sub["축제명"],
        #                     y=df_sub["업소수"],
        #                     name=유형,
        #                     marker_color=color_list[i % len(color_list)],
        #                     yaxis="y"  # 기본값이라 생략 가능
        #                 ))

        #             # ✅ 방문객 수 점 그래프 (오른쪽 y축)
        #             visitor_dict = df_info.set_index("축제명")["일일방문객(명)"].to_dict()
        #             visitor_raw = [visitor_dict.get(f, 0) for f in 비교축제들]

        #             fig.add_trace(go.Scatter(
        #                 x=비교축제들,
        #                 y=visitor_raw,
        #                 mode="markers+text",
        #                 name="일일 방문객 수",
        #                 text=[f"{v:,.0f}명" for v in visitor_raw],
        #                 textposition="top center",
        #                 marker=dict(size=12, color="black", symbol="diamond"),
        #                 yaxis="y2"
        #             ))
        
        #             # ✅ 이중 y축 설정
        #             fig.update_layout(
        #                 barmode="stack",
        #                 title=f"{선택축제} vs 유사 축제: 인프라 + 방문객 수 비교",
        #                 xaxis_title="축제명",
        #                 yaxis=dict(
        #                     title="숙소/식당 수",
        #                     side="left"
        #                 ),
        #                 yaxis2=dict(
        #                     title="일일 방문객 수 (명)",
        #                     overlaying="y",
        #                     side="right",
        #                     range=[0, 40000],
        #                     showgrid=False
        #                 ),
        #                 legend_title="항목",
        #                 height=550
        #             )
        
        #             return fig
        
