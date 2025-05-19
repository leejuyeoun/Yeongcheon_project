from shiny.express import ui, input, render
from shinywidgets import render_plotly
import plotly.express as px
import pathlib
import pandas as pd

# ✅ 경로 설정
base_dir = pathlib.Path(__file__).parent

# ✅ 데이터 불러오기
df_info = pd.read_excel(base_dir / "축제정보.xlsx")
df_compare = pd.read_excel(base_dir / "축제비교대상선정이유.xlsx")
df_infra_summary = pd.read_excel(base_dir / "인프라요약_전처리결과.xlsx")
df_bar_long = pd.read_excel(base_dir / "인프라그래프데이터_전처리결과.xlsx")

# ✅ 표 1: 축제 기본정보
df_info["일일 평균 방문객"] = (df_info["총방문객(명)"] / df_info["일수(일)"]).round(1)
df_info_display = df_info[["축제명", "지역", "일수(일)", "총방문객(명)", "일일 평균 방문객", "개최시기(월)"]]

# ✅ 표 2: 비교대상 선정이유
df_compare_display = df_compare.rename(columns={"비교이유": "비교 이유"})[["영천축제", "비교축제", "비교 이유"]]

# ✅ Overview 탭 UI 구성
ui.page_opts(title="영천시 축제 대시보드", fillable=True)

with ui.navset_pill(id="tab"):
    with ui.nav_panel("Overview"):
        # ▶ 위쪽: 표 1, 2
        with ui.layout_columns(col_widths=(6, 6)):
            with ui.card(full_screen=True):
                ui.h4("1. 기본 정보 요약표")
                @render.data_frame
                def info_table():
                    return df_info_display

            with ui.card(full_screen=True):
                ui.h4("2. 비교대상 선정 이유")
                @render.data_frame
                def compare_table():
                    return df_compare_display

        # ▶ 아래쪽: 표 3, 그래프 4
        with ui.layout_columns(col_widths=(6, 6)):
            with ui.card(full_screen=True):
                ui.h4("3. 인프라 요약표")
                @render.data_frame
                def infra_table():
                    return df_infra_summary

            with ui.card(full_screen=True):
                ui.h4("3-1. 인프라 막대그래프")
                ui.input_radio_buttons(
                    id="infra_type",
                    label="업소 유형 선택",
                    choices=["식당", "숙소"],
                    selected="식당",
                    inline=True
                )

                @render_plotly
                def infra_bar():
                    df_filtered = df_bar_long[df_bar_long["업소유형"] == input.infra_type()]
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


    with ui.nav_panel("Map View"):
        with ui.layout_columns(col_widths=(6, 6)):

            with ui.card():
                ui.h4("왼쪽 지도")
                @render.ui
                def map_left():
                    return ui.HTML(
                        '<iframe src="/영천시_축제_인프라.html" width="100%" height="600px" style="border:none;"></iframe>'
                    )

            with ui.card():
                ui.h4("오른쪽 지도")
                @render.ui
                def map_right():
                    return ui.HTML(
                        '<iframe src="/영천시_축제_인프라.html" width="100%" height="600px" style="border:none;"></iframe>'
                    )




    with ui.nav_panel("Stats View"):
        # ✅ 데이터 로딩
        df_stats = pd.read_excel(base_dir / "영천시_숙소_식당_카페_주차장_분리.xlsx")
        축제_목록 = sorted(df_stats["축제명"].dropna().unique().tolist())
        숙소_세부 = sorted(df_stats[df_stats["구분1"] == "숙소"]["구분2"].dropna().unique().tolist())
        식당_세부 = sorted(df_stats[df_stats["구분1"] == "식당"]["구분2"].dropna().unique().tolist())
    
        # ✅ 🔧 깔끔한 필터 카드 레이아웃
        with ui.layout_column_wrap(width="300px"):
            with ui.card():
                ui.h5("🎯 축제를 선택하세요")
                ui.input_select(
                    id="selected_festival",
                    label=None,
                    choices=축제_목록,
                    selected=축제_목록[0],
                    multiple=False,
                    width="100%"
                )
    
            with ui.card():
                ui.h5("🏨 숙소 구분2")
                ui.input_checkbox_group(
                    id="숙소세부",
                    label=None,
                    choices=숙소_세부,
                    selected=숙소_세부
                )
    
            with ui.card():
                ui.h5("🍽️ 식당 구분2")
                ui.input_checkbox_group(
                    id="식당세부",
                    label=None,
                    choices=식당_세부,
                    selected=식당_세부
                )
    
        # ✅ 📊 그래프 4개 깔끔하게 정렬
        with ui.layout_columns(col_widths=(6, 6)):
            with ui.card():
                ui.h4("🏨 숙소 구분2 분포")
                @render_plotly
                def 숙소차트():
                    df = df_stats[
                        (df_stats["축제명"] == input.selected_festival()) &
                        (df_stats["구분1"] == "숙소") &
                        (df_stats["구분2"].isin(input.숙소세부()))
                    ]
                    count = df["구분2"].value_counts().reset_index()
                    count.columns = ["구분2", "수"]
                    return px.pie(count, names="구분2", values="수", title="숙소 세부유형") if not count.empty else px.pie(names=["없음"], values=[1], title="숙소 데이터 없음")
    
            with ui.card():
                ui.h4("🍽️ 식당 구분2 분포")
                @render_plotly
                def 식당차트():
                    df = df_stats[
                        (df_stats["축제명"] == input.selected_festival()) &
                        (df_stats["구분1"] == "식당") &
                        (df_stats["구분2"].isin(input.식당세부()))
                    ]
                    count = df["구분2"].value_counts().reset_index()
                    count.columns = ["구분2", "수"]
                    return px.pie(count, names="구분2", values="수", title="식당 세부유형") if not count.empty else px.pie(names=["없음"], values=[1], title="식당 데이터 없음")
    
        with ui.layout_columns(col_widths=(6, 6)):
            with ui.card():
                ui.h4("☕ 카페 구분2 분포")
                @render_plotly
                def 카페차트():
                    df = df_stats[
                        (df_stats["축제명"] == input.selected_festival()) &
                        (df_stats["구분1"] == "카페")
                    ]
                    count = df["구분2"].value_counts().reset_index()
                    count.columns = ["구분2", "수"]
                    return px.pie(count, names="구분2", values="수", title="카페 세부유형") if not count.empty else px.pie(names=["없음"], values=[1], title="카페 데이터 없음")
    
            with ui.card():
                ui.h4("🅿️ 주차장 구분2 분포")
                @render_plotly
                def 주차장차트():
                    df = df_stats[
                        (df_stats["축제명"] == input.selected_festival()) &
                        (df_stats["구분1"] == "주차장")
                    ]
                    count = df["구분2"].value_counts().reset_index()
                    count.columns = ["구분2", "수"]
                    return px.bar(count, x="구분2", y="수", title="주차장 세부유형") if not count.empty else px.bar(title="주차장 데이터 없음")
    

    with ui.nav_panel("Insight View"):
        "💡 인사이트 도출 페이지입니다."

