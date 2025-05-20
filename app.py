from shiny.express import ui, input, render
from shinywidgets import render_plotly
import plotly.express as px
import pathlib
import pandas as pd

# 데이터 로드
from shared import df_info, df_compare, df_infra_summary, df_bar_long, df_infra_combined, df_stats, df_infra_merged

# ✅ HTML 파일 매핑
축제_파일_매핑 = {
    "작약꽃축제": "작약꽃축제.html",
    "와인페스타": "와인페스타.html",
    "별빛축제": "별빛축제.html",
    "벚꽃축제": "벚꽃축제.html",
    "오미자축제": "오미자축제.html",
    "우주항공축제": "우주항공축제.html"
}


# ✅ 표 1: 축제 기본정보 (작약꽃축제 통합 버전)
df_info["일일 평균 방문객"] = (df_info["총방문객(명)"] / df_info["일수(일)"]).round(1)
df_info_fixed = df_info.copy()
df_info_fixed.loc[df_info_fixed["축제명"].isin(["작약꽃축제A", "작약꽃축제B", "작약꽃축제C"]), "축제명"] = "작약꽃축제(A/B/C)"
df_info_display = df_info_fixed.drop_duplicates(subset="축제명")[
    ["축제명", "지역", "일수(일)", "총방문객(명)", "일일 평균 방문객", "개최시기(월)"]
].reset_index(drop=True)


# ✅ Overview 탭 UI 구성
ui.page_opts(title="영천시 축제 대시보드", fillable=True)


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
            @render.ui
            def compare_custom():
                return ui.HTML("""
                <div style="display: flex; flex-direction: column; gap: 2rem; font-family: sans-serif; font-size: 14px;">

                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="flex: 1; background: #f2f2f2; padding: 1rem; border-radius: 10px;">
                            <strong>작약꽃축제</strong><br>
                            일일 평균 방문객: 7,142.9명
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
                            일일 평균 방문객: 16,666.7명
                        </div>
                    </div>

                </div>
                """)

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
                choices=["숙소", "식당"],
                selected="숙소",
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
    ui.p("좌우 지도를 통해 서로 다른 축제를 선택하고 인프라(숙소, 식당, 카페 등)를 비교", style="font-size: 16px; color: #555;")
    with ui.layout_columns(col_widths=(6, 6)):
        with ui.card():
            ui.h4("📍 왼쪽 지도 (선택한 축제 위치)")
            ui.input_select("left_festival", "🎯 왼쪽 지도: 축제를 선택하세요", list(축제_파일_매핑.keys()), selected="작약꽃축제")
            @render.ui
            def map_left():
                filename = 축제_파일_매핑[input.left_festival()]
                return ui.HTML(f'<iframe src="/{filename}" width="100%" height="600px" style="border:none;"></iframe>')

        with ui.card():
            ui.h4("📍 오른쪽 지도 (선택한 축제 위치)")
            ui.input_select("right_festival", "🎯 오른쪽 지도: 축제를 선택하세요", list(축제_파일_매핑.keys()), selected="와인페스타")
            @render.ui
            def map_right():
                filename = 축제_파일_매핑[input.right_festival()]
                return ui.HTML(f'<iframe src="/{filename}" width="100%" height="600px" style="border:none;"></iframe>')


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
                label="🏨 숙소 구분2",
                choices=숙소_세부,
                selected=숙소_세부
            )
            ui.input_checkbox_group(
                id="식당세부",
                label="🍽️ 식당 구분2",
                choices=식당_세부,
                selected=식당_세부
            )

        # ✅ 📊 그래프 3개 깔끔하게 정렬
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
            # 카페 차트는 제거됨
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