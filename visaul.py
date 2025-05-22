import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Haversine 거리 계산 (단위: km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# 데이터 로드
file_facilities = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\전체_숙소_식당_카페_주차장_통합-최종.xlsx"
file_festival = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\축제정보.xlsx"

facilities_df = pd.read_excel(file_facilities)
festival_df = pd.read_excel(file_festival)

# 사용할 시설
facility_types = ["숙소", "식당", "카페", "주차장"]

# 반경 설정 (km)
radius_km = 10

# 반경 내 시설 수 및 비율 계산
for facility in facility_types:
    filtered = facilities_df[facilities_df["구분1"] == facility].copy()
    facility_lats = filtered["위도"].values
    facility_lons = filtered["경도"].values

    counts = []
    for _, fest in festival_df.iterrows():
        fest_lat, fest_lon = fest["위도"], fest["경도"]
        distances = haversine(fest_lat, fest_lon, facility_lats, facility_lons)
        count_within_radius = np.sum(distances <= radius_km)
        counts.append(count_within_radius)

    festival_df[f"{facility}수"] = counts
    festival_df[f"{facility}비율"] = festival_df[f"{facility}수"] / festival_df["일일방문객(명)"]

# 축제별 상대 점수 계산 (자기 축제 내 최대 비율 기준 정규화)
relative_scores = []
for _, row in festival_df.iterrows():
    values = [row[f"{f}비율"] for f in facility_types]
    max_val = max(values)
    if max_val == 0:
        normalized = [0] * len(values)
    else:
        normalized = [5 * (v / max_val) for v in values]
    relative_scores.append(normalized)

# 레이더 차트용 카테고리 (닫기용 첫 항목 반복)
categories = facility_types + [facility_types[0]]

# Plotly 레이더 차트
fig = go.Figure()

for i, (row, score) in enumerate(zip(festival_df.itertuples(), relative_scores)):
    values = score + score[:1]  # 닫기용 복사
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=row.축제명,
        visible=(i == 0)  # 첫 축제만 보이게
    ))

# 드롭다운 버튼 생성
buttons = []
for i, row in festival_df.iterrows():
    visible_array = [False] * len(festival_df)
    visible_array[i] = True
    buttons.append(dict(label=row["축제명"],
                        method="update",
                        args=[{"visible": visible_array},
                              {"title": f"{row['축제명']} 인프라 상대 점수 레이더 차트"}]))

# 레이아웃 설정
fig.update_layout(
    title=f"{festival_df.iloc[0]['축제명']} 인프라 상대 점수 레이더 차트",
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        x=1.15,
        y=1.15
    )]
)

# 차트 표시
fig.show()

# =================================================
import pandas as pd
import numpy as np
import plotly.express as px

# 파일 경로
file_facilities = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\전체_숙소_식당_카페_주차장_통합-최종.xlsx"
file_festival = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\축제정보.xlsx"

# 데이터 로드
facilities_df = pd.read_excel(file_facilities)
festival_df = pd.read_excel(file_festival)

# 시설 종류
facility_types = ["숙소", "식당", "카페", "주차장"]

# Haversine 거리 계산 함수
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# 반경 설정
radius_km = 10

# 시설 수 계산
for facility in facility_types:
    filtered = facilities_df[facilities_df["구분1"] == facility]
    lats = filtered["위도"].values
    lons = filtered["경도"].values
    counts = []
    for _, fest in festival_df.iterrows():
        dist = haversine(fest["위도"], fest["경도"], lats, lons)
        counts.append(np.sum(dist <= radius_km))
    festival_df[f"{facility}수"] = counts

# 식당 수 기준 산점도
fig1 = px.scatter(
    festival_df,
    x="식당수",
    y="일일방문객(명)",
    text="축제명",
    title="식당 수 vs 일일 방문객 수",
    labels={"식당수": "식당 수", "일일방문객(명)": "일일 방문객 수"}
)
fig1.update_traces(textposition="top center")
fig1.update_layout(
    showlegend=False,
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=25,
        range=[0, 100]  # 필요 시 조정 가능
    )
)
fig1.show()
# 숙소 수 기준 산점도
fig2 = px.scatter(
    festival_df,
    x="숙소수",
    y="일일방문객(명)",
    text="축제명",
    title="숙소 수 vs 일일 방문객 수",
    labels={"숙소수": "숙소 수", "일일방문객(명)": "일일 방문객 수"}
)
fig2.update_traces(textposition="top center")
fig2.update_layout(showlegend=False)
fig2.show()

# 숙소 + 식당 수 기준 산점도
festival_df["숙소+식당수"] = festival_df["숙소수"] + festival_df["식당수"]
fig3 = px.scatter(
    festival_df,
    x="숙소+식당수",
    y="일일방문객(명)",
    text="축제명",
    title="숙소+식당 수 vs 일일 방문객 수",
    labels={"숙소+식당수": "숙소+식당 수", "일일방문객(명)": "일일 방문객 수"}
)
fig3.update_traces(textposition="top center")
fig3.update_layout(
    showlegend=False,
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=25,
        range=[0, 150]  # 필요 시 조정 가능
    )
)
fig3.show()

#=================
# 개선 우선순위 도출 (축제별 부족 인프라 TOP1~2 강조)


#방문객 대비 인프라 비율 계산
festival_df[f"{facility}비율"] = festival_df[f"{facility}수"] / festival_df["일일방문객(명)"]

# 정규화 함수 (0~5점)
def normalize_series(series):
    return 5 * (series - series.min()) / (series.max() - series.min())

# 시설 종류
facility_types = ["숙소", "식당", "카페", "주차장"]

# 비율 및 점수 계산
for facility in facility_types:
    festival_df[f"{facility}비율"] = festival_df[f"{facility}수"] / festival_df["일일방문객(명)"]
    festival_df[f"{facility}점수"] = normalize_series(festival_df[f"{facility}비율"])


## 축제별 인프라 점수 차이 분석
# 평균 점수 계산
mean_scores = {f: festival_df[f"{f}점수"].mean() for f in facility_types}

# 각 축제별 부족 점수 계산 (평균 - 현재 점수)
for f in facility_types:
    festival_df[f"{f}부족도"] = mean_scores[f] - festival_df[f"{f}점수"]

# 개선 우선순위 추출
def get_top_n_shortages(row, n=2):
    scores = {f: row[f"{f}부족도"] for f in facility_types}
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_items[:n]]

festival_df["개선우선순위"] = festival_df.apply(get_top_n_shortages, axis=1)

# 결과 확인
print(festival_df[["축제명", "개선우선순위"]])



# ============================
# 숙소 및 식당 상위 및 하위 개수(가로 막대그래프)
import pandas as pd
import plotly.express as px

# 분석할 인프라 컬럼들
infra_columns = ["숙소수", "식당수"]


top_n = 5  # 상위/하위 몇 개 보여줄지

for col in infra_columns:
    # ⬛ 상위 N
    top_df = festival_df.sort_values(by=col, ascending=False).head(top_n)
    fig_top = px.bar(
        top_df,
        x=col,
        y="축제명",
        orientation="h",
        title=f"{col} 상위 {top_n} 축제",
        labels={col: col, "축제명": "축제명"},
        text=col,
        color=col,
        color_continuous_scale="Blues"
    )
    fig_top.update_layout(yaxis=dict(autorange="reversed"))
    fig_top.show()

    # ⬛ 하위 N
    bottom_df = festival_df.sort_values(by=col, ascending=True).head(top_n)
    fig_bottom = px.bar(
        bottom_df,
        x=col,
        y="축제명",
        orientation="h",
        title=f"{col} 하위 {top_n} 축제",
        labels={col: col, "축제명": "축제명"},
        text=col,
        color=col,
        color_continuous_scale="Reds"
    )
    fig_bottom.update_layout(yaxis=dict(autorange="reversed"))
    fig_bottom.show()

##=============================================================
# 05/21
import pandas as pd
from geopy.distance import geodesic
from geopy.exc import GeopyError

# 파일 경로
festival_path = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\축제정보.xlsx"
infra_path = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\전체_숙소_식당_카페_주차장_통합-최종.xlsx"

# 데이터 로드
festival_df = pd.read_excel(festival_path)
infra_df = pd.read_excel(infra_path)

# 대분류 매핑
category_mapping = {
    '숙소': ['호텔', '모텔', '게하', '여관', '펜션', '캠핑'],
    '식당': ['한식', '중식', '일식', '양식', '분식', '해외음식', '뷔페', '주점', '치킨']
}

def map_category(sub):
    for main_cat, sub_list in category_mapping.items():
        if str(sub).strip() in sub_list:
            return main_cat
    return None

infra_df['대분류'] = infra_df['구분2'].apply(map_category)

# 거리 3km 이내 인프라 개수 집계 + 세부 분류
infra_summary = []

for _, fest in festival_df.iterrows():
    fest_coord = (fest['위도'], fest['경도'])
    nearby = []
    nearby_detail = []

    for _, infra in infra_df.iterrows():
        try:
            infra_coord = (infra['위도'], infra['경도'])
            if geodesic(fest_coord, infra_coord).km <= 3:
                main_cat = infra['대분류']
                sub_cat = infra['구분2']
                if main_cat is not None:
                    nearby.append(main_cat)
                    nearby_detail.append((main_cat, sub_cat))
        except (GeopyError, ValueError, TypeError):
            continue

    # 대분류 개수
    count_dict = {cat: nearby.count(cat) for cat in category_mapping}
    count_dict['축제명'] = fest['축제명']
    count_dict['지역'] = fest['지역']
    count_dict['일일방문객(명)'] = fest['일일방문객(명)']
    count_dict['세부리스트'] = nearby_detail
    infra_summary.append(count_dict)

summary_df = pd.DataFrame(infra_summary)

# 점수 계산
def normalize(series):
    if series.max() == series.min():
        return pd.Series([0] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min()) * 5

for cat in category_mapping:
    summary_df[f'{cat}비율'] = summary_df[cat] / summary_df['일일방문객(명)']
    summary_df[f'{cat}점수'] = normalize(summary_df[f'{cat}비율'].fillna(0))

# 부족 인프라 Top2 및 세부 분류 추출
def get_top_shortages_with_detail(row):
    scores = {cat: row.get(f"{cat}점수", 0) for cat in category_mapping}
    sorted_short = sorted(scores.items(), key=lambda x: x[1])
    top2 = sorted_short[:2]

    details = {main: [] for main in category_mapping}
    if isinstance(row['세부리스트'], list):
        for main_cat, sub_cat in row['세부리스트']:
            if main_cat in details:
                details[main_cat].append(sub_cat)

    def get_least_common(sub_list):
        return pd.Series(sub_list).value_counts().idxmin() if sub_list else None

    top1_main, top2_main = top2[0][0], top2[1][0]
    top1_detail = get_least_common(details[top1_main])
    top2_detail = get_least_common(details[top2_main])

    return pd.Series([top1_main, top1_detail, top2_main, top2_detail],
                     index=['부족1', '부족1_세부', '부족2', '부족2_세부'])

# 최종 결과 생성
shortages_df = summary_df[['축제명', '지역', '세부리스트'] + list(category_mapping.keys()) + ['일일방문객(명)']].copy()
shortages_df[['부족1', '부족1_세부', '부족2', '부족2_세부']] = summary_df.apply(get_top_shortages_with_detail, axis=1)

# 최종 결과 출력
result_df = shortages_df[['축제명', '지역', '부족1', '부족1_세부', '부족2', '부족2_세부']].reset_index(drop=True)
print(result_df)


