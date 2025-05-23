from shiny.express import ui, input, render
from shinywidgets import render_plotly
import plotly.express as px
import pathlib
import pandas as pd
from plotly import graph_objects as go
from shiny import reactive

from shinyswatch import theme
ui.page_opts(title="영천시 축제 인프라 분석", theme=theme.minty, fillable=False)

# 데이터 로드
from shared import df_info, df_compare, df_infra_summary, df_bar_long, df_infra_combined, df_stats, df_infra_merged

#  HTML 파일 매핑
축제_파일_매핑 = {
    "작약꽃축제": "작약꽃축제_.html",
    "와인페스타": "와인페스타_.html",
    "별빛축제": "별빛축제_.html",
    "벚꽃축제": "벚꽃축제_.html",
    "오미자축제": "오미자축제_.html",
    "우주항공축제": "우주항공축제.html"
}


#  표 1: 축제 기본정보 (작약꽃축제 통합 버전)
df_info["일일 평균 방문객"] = (df_info["총방문객(명)"] / df_info["일수(일)"]).round(0)
df_info_fixed = df_info.copy()
df_info_fixed.loc[df_info_fixed["축제명"].isin(["작약꽃축제A", "작약꽃축제B", "작약꽃축제C"]), "축제명"] = "작약꽃축제(A/B/C)"
df_info_display = df_info_fixed.drop_duplicates(subset="축제명")[
    ["축제명", "지역", "일수(일)", "총방문객(명)", "일일 평균 방문객", "개최시기(월)"]
].reset_index(drop=True)


with ui.nav_panel("OverView"):
    ui.h2(" 축제 한눈에 보기", style="margin-bottom: 2rem;")

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
                    Shiny.setInputValue("__nav_festival_snapshot__", "Festival Infra", {priority: "event"});
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
        ui.HTML("""<div class="festival-card hover-card" style="background-color: #FAFAFA; border: 2px solid #DB6C7E; border-radius: 10px; overflow: hidden; font-family: sans-serif; color: #DB6C7E;">
            <div style="background-color: #DB6C7E; color: white; padding: 0.8rem 1.2rem; font-size: 1.3rem; font-weight: bold;">
                작약꽃축제
            </div>
            <div style="height: 300px; border-bottom: 2px solid #DB6C7E;">
                <img src="peony.jpg" alt="작약꽃축제" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div style="display: flex; align-items: center; justify-content: center;">
                <img src="peonyinfo.jpg" style="width: 100%; object-fit: contain;">
            </div>
        </div>""")

        ui.HTML("""<div class="festival-card hover-card" style="background-color: #FAFAFA; border: 2px solid #8d6e63; border-radius: 10px; overflow: hidden; font-family: sans-serif; color: #8d6e63;">
            <div style="background-color: #8d6e63; color: white; padding: 0.8rem 1.2rem; font-size: 1.3rem; font-weight: bold;">
                와인페스타
            </div>
            <div style="height: 300px; border-bottom: 2px solid #8d6e63;">
                <img src="wine.jpg" alt="와인페스타" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div>
                <img src="wineinfo.jpg" alt="와인페스타 정보" style="width: 100%; object-fit: contain;">
            </div>
        </div>""")

        ui.HTML("""<div class="festival-card hover-card" style="background-color: #FAFAFA; border: 2px solid #745D8E; border-radius: 10px; overflow: hidden; font-family: sans-serif; color: #745D8E;">
            <div style="background-color: #745D8E; color: white; padding: 0.8rem 1.2rem; font-size: 1.3rem; font-weight: bold;">
                별빛축제
            </div>
            <div style="height:300px; border-bottom: 2px solid #745D8E;">
                <img src="starlight.jpg" alt="별빛축제" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div>
                <img src="starlightinfo.jpg" alt="별빛축제 정보" style="width: 100%; object-fit: contain;">
            </div>
        </div>""")

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

    ui.HTML("""
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            document.querySelectorAll(".hover-card").forEach(function(card) {
                card.addEventListener("click", function() {
                    const tab = document.querySelector('a[data-value="Festival Infra"]');
                    if (tab) tab.click();
                });
            });
        });
    </script>
    """)

    ui.HTML("""
    <script>
        setTimeout(function() {
            const btn = document.getElementById("compare_button");
            if (btn) {
                btn.onclick = function() {
                    const tab = document.querySelector('a[data-value="Festival Compare"]');
                    if (tab) tab.click();
                    btn.blur();
                };
            }
        }, 300);
    </script>
    """)






with ui.nav_panel("Festival Compare"):
    # 제목 + 버튼을 같은 줄에 배치
    with ui.layout_columns(col_widths=(5, 2, 2, 2)):  # 제목:5, 버튼3개
        ui.h4("유사 축제 인프라 비교", style="margin-top: 1rem; color: #444;")

        ui.input_action_button("btn1", "작약꽃 vs 벚꽃")
        ui.input_action_button("btn2", "와인 vs 오미자")
        ui.input_action_button("btn3", "별빛 vs 우주항공")

        #  작약꽃 vs 벚꽃
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
              <th>항목</th>
              <th>작약꽃축제 (영천)</th>
              <th>벚꽃축제 (옥정호)</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>시기</td><td>5월</td><td>4월</td></tr>
            <tr><td>기간</td><td>7일</td><td>2일</td></tr>
            <tr><td>총방문객</td><td>50,000명</td><td>35,000명</td></tr>
            <tr><td>일일평균</td><td>7,143명</td><td>17,500명</td></tr>
            <tr><td>지역특징</td><td>대구 근교</td><td>옥정호(아름다운 길 100선 선정)</td></tr>
            <tr><td>인프라</td><td>푸드트럭/행사 미운행</td><td>먹거리 풍부/행사 진행</td></tr>
          </tbody>
        </table>
                """),
                title="작약꽃축제 vs 벚꽃축제 비교",
                easy_close=True,
                footer=None,
                class_="modal-xl"
            )
            ui.modal_show(m)


        # 와인 vs 오미자
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
            <tr><td>시기</td><td>10월</td><td>9월</td></tr>
            <tr><td>기간</td><td>2일</td><td>3일</td></tr>
            <tr><td>총방문객</td><td>40,000명</td><td>50,000명</td></tr>
            <tr><td>일일평균</td><td>20,000명</td><td>16,667명</td></tr>
            <tr><td>지역특징</td><td>시내 중심</td><td>시골 변방</td></tr>
            <tr><td>인프라</td><td>인프라 풍부</td><td>먹거리 부족</td></tr>
          </tbody>
        </table>
                """),
                title="와인페스타 vs 오미자축제 비교",
                easy_close=True,
                footer=None,
                class_="modal-xl"
            )
            ui.modal_show(m)

        # 별빛 vs 우주항공
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
            <tr><td>시기</td><td>10월</td><td>5월</td></tr>
            <tr><td>기간</td><td>3일</td><td>4일</td></tr>
            <tr><td>총방문객</td><td>60,000명</td><td>120,000명</td></tr>
            <tr><td>일일평균</td><td>20,000명</td><td>30,000명</td></tr>
            <tr><td>지역특징</td><td>보현산 정상</td><td>반도</td></tr>
            <tr><td>인프라</td><td>숙소/식당 부족</td><td>인프라 풍부</td></tr>
          </tbody>
        </table>
                """),
                title="별빛축제 vs 우주항공축제 비교",
                easy_close=True,
                footer=None,
                class_="modal-xl"
            )
            ui.modal_show(m)

    ui.p("아래에서 두 개의 축제를 선택하고 위치 및 인프라를 비교하세요.", style="font-size: 15px; color: #666;")


    # 축제 선택 필터
    with ui.layout_columns(col_widths=(6, 6)):
        with ui.card():
            ui.h5("영천 축제 선택", style="color: #333;")
            ui.input_select("left_festival", "왼쪽 지도: 축제를 선택하세요", list(축제_파일_매핑.keys()), selected="작약꽃축제")
        # 왼쪽 축제의 방문객 수 출력
            @render.text
            def left_visitors():
                # 작약꽃축제 A/B/C 통합 처리 포함
                selected = input.left_festival()
                selected_mapped = (
                    "작약꽃축제(A/B/C)" if "작약꽃축제" in selected else selected
                )

                row = df_info_display[df_info_display["축제명"] == selected_mapped]
                if not row.empty:
                    count = int(row.iloc[0]["일일 평균 방문객"])
                    return f"일일 평균 방문객 수: 약 {count:,}명"
                else:
                    return "일일 평균 방문객 수: 정보 없음"
                
        with ui.card():
            ui.h5("비교 축제 선택", style="color: #333;")
            ui.input_select("right_festival", "오른쪽 지도: 축제를 선택하세요", list(축제_파일_매핑.keys()), selected="벚꽃축제")
            # 오른쪽쪽 축제의 방문객 수 출력
            @render.text
            def right_visitors():
                # 작약꽃축제 A/B/C 통합 처리 포함
                selected = input.right_festival()
                selected_mapped = (
                    "작약꽃축제(A/B/C)" if "작약꽃축제" in selected else selected
                )

                row = df_info_display[df_info_display["축제명"] == selected_mapped]
                if not row.empty:
                    count = int(row.iloc[0]["일일 평균 방문객"])
                    return f"일일 평균 방문객 수: 약 {count:,}명"
                else:
                    return "일일 평균 방문객 수: 정보 없음"


    # 지도 및 인프라 요약 정보
    with ui.layout_columns(col_widths=(6, 6)):
        with ui.card():
            ui.h5("영천 축제 위치 지도")
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
            ui.h5("비교 축제 위치 지도")
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

    with ui.layout_columns(col_widths=(12,)):
        with ui.card():
            ui.h5("주요 인프라 항목 수 비교", style="margin-top: 1rem; text-align: center;")  # 제목도 가운데 정렬

            # 그래프를 가운데 정렬하기 위한 div 래퍼 추가
            with ui.div(style="display: flex; justify-content: center;"):

                @render_plotly
                def infra_compare_bar():
                    # ⬇ 데이터 준비
                    left = input.left_festival()
                    right = input.right_festival()
                    df = df_infra_merged.copy()
                    df = df[df["구분1"].isin(["숙소", "식당", "화장실", "주차장"])]

                    summary = df[df["축제명"].str.contains(left, na=False)].groupby("구분1").size().reset_index(name=left)
                    summary2 = df[df["축제명"].str.contains(right, na=False)].groupby("구분1").size().reset_index(name=right)
                    merged = pd.merge(summary, summary2, on="구분1", how="outer").fillna(0)

                    df_plot = pd.melt(merged, id_vars="구분1", var_name="축제명", value_name="개수")

                    # ⬇ 그래프 생성
                    fig = px.bar(
                        df_plot,
                        x="구분1",
                        y="개수",
                        color="축제명",
                        barmode="group",
                        text="개수",
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )

                    fig.update_traces(textposition="outside")

                    fig.update_layout(
                        height=450,
                        width=960,  # 카드 너비에 맞춰 넓게
                        bargap=0.2,
                        xaxis_title="인프라 유형",
                        font=dict(size=16),
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

                    return fig  # 반드시 fig 객체만 반환
        
    # 세부 유형 막대그래프
    with ui.layout_columns(col_widths=[6, 6]):  # 카드 너비 균등 조절
        with ui.card():
            ui.h5("영천 축제 인프라 세부 유형")
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
                    xaxis_tickangle=-30,  # x축 라벨 겹침 방지
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
            ui.h5("비교 축제 인프라 세부 유형")
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













with ui.nav_panel("Festival Infra"):
    # 데이터 로딩
    축제_목록 = sorted(df_stats["축제명"].dropna().unique().tolist())
    숙소_세부 = sorted(df_stats[df_stats["구분1"] == "숙소"]["구분2"].dropna().unique().tolist())
    식당_세부 = sorted(df_stats[df_stats["구분1"] == "식당"]["구분2"].dropna().unique().tolist())

# 버튼 추가 (오른쪽 정렬)
    with ui.div(
        style="display: flex; justify-content: flex-end; margin: -0.3rem 0 0.5rem 0;"
    ):
        ui.input_action_button(
            id="go_to_map_from_stats",
            label="유사 축제와 비교하기",
            class_="btn btn-lg",
            style=(
                "font-size: 15px; padding: 0.6rem 1.2rem; "
                "border-radius: 10px; font-weight: bold; "
                "background-color: #5a7dad; color: white; border: none;"
            )
        )

    # 탭 이동 JS 코드 (Map View → Festival Compare로 변경)
    ui.HTML("""
    <script>
    document.addEventListener("DOMContentLoaded", function () {
        const btn = document.getElementById("go_to_map_from_stats");
        if (btn) {
            btn.onclick = function () {
                const selected = document.querySelector('select#selected_festival')?.value;

                const tab = document.querySelector('a[data-value="Festival Compare"]');
                if (tab) tab.click();

                setTimeout(function () {
                    const leftDropdown = document.querySelector('select#left_festival');
                    const rightDropdown = document.querySelector('select#right_festival');
                    if (!leftDropdown || !rightDropdown) return;

                    if (["별빛축제", "우주항공축제"].includes(selected)) {
                        leftDropdown.value = "별빛축제";
                        rightDropdown.value = "우주항공축제";
                    } else if (["와인페스타", "오미자축제"].includes(selected)) {
                        leftDropdown.value = "와인페스타";
                        rightDropdown.value = "오미자축제";
                    } else if (
                        ["작약꽃축제A", "작약꽃축제B", "작약꽃축제C", "작약꽃축제(A/B/C)", "벚꽃축제"].includes(selected)
                    ) {
                        leftDropdown.value = "작약꽃축제";
                        rightDropdown.value = "벚꽃축제";
                    }

                    leftDropdown.dispatchEvent(new Event("change", { bubbles: true }));
                    rightDropdown.dispatchEvent(new Event("change", { bubbles: true }));
                }, 500);
            };
        }
    });
    </script>
    """)


    # 사이드바 및 본문 레이아웃
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

                    # 비율 계산
                    if not count.empty:
                        count["percent"] = (count["수"] / count["수"].sum() * 100).round(1)
                        count["label"] = count["percent"].astype(str) + "% (" + count["수"].astype(str) + "개)"
                    else:
                        count = pd.DataFrame({'구분2': ["없음"], "수": [1], "label": ["없음"]})

                    fig = px.pie(
                        count,
                        names="구분2",
                        values="수",
                        title="어떤 유형의 숙소가 더 많을까?",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    );

                    fig.update_traces(
                        text=count["label"],  # custom label 적용
                        textinfo="text",
                        textposition='outside',
                        textfont_size=15
                    )

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

                    # 라벨 텍스트 생성: 비율 + 수 + "개"
                    if not count.empty:
                        count["percent"] = (count["수"] / count["수"].sum() * 100).round(1)
                        count["label"] = count["percent"].astype(str) + "% (" + count["수"].astype(str) + "개)"
                    else:
                        count = pd.DataFrame({"구분2": ["없음"], "수": [1], "label": ["없음"]})

                    fig = px.pie(
                        count,
                        names="구분2",
                        values="수",
                        title="어떤 종류의 식당이 더 많을까?",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    );

                    fig.update_traces(
                        text=count["label"],  # 커스텀 텍스트 적용
                        textinfo="text",
                        textposition="outside",
                        textfont_size=text_size
                    )

                    return fig



                
        with ui.layout_columns(col_widths=(6, 6)):
            # 왼쪽: 공중화장실 수 그래프
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

            # 오른쪽: 공영주차장 수 그래프 (기존 코드 그대로)
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
                    

        
