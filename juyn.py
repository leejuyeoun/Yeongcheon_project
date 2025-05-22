# 5/13 ~ 23
import pandas as pd
import numpy as np

# 데이터 전처리
## 각 파일 칼럼명 통일 / 필요없는 칼럼 제거 / 지역, 축제명 칼럼 추가 
### <지역>	업소명	위도	경도	구분1	구분2	주소
import os
import pandas as pd

os.chdir(r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터")

df = pd.read_excel("영천시_숙박업 현황_위도경도.xlsx")
df = df.rename(columns={"영업장주소(도로명)" : "주소",
           'Latitude' : "위도",
           "Longitude" : "경도"})
df = df[['업소명', '위도', '경도', '구분1', '구분2', '주소']]

df2 = pd.read_excel("영천시_농어촌민박_위도경도_구분.xlsx")
df2 = df2.rename(columns={"도로명전체주소" : "주소",
           '좌표정보(X)' : "위도",
           "좌표정보(Y)" : "경도",
           "사업장명" :"업소명"})
df2 = df2[['업소명', '위도', '경도', '구분1', '구분2', '주소']]

df3 = pd.read_excel("영천시_캠핑장 현황_위도경도_구분.xlsx")
df3 = df3.rename(columns={"상호" : "업소명",
           'Latitude' : "위도",
           "Longitude" : "경도"})
df3 = df3[['업소명', '위도', '경도', '구분1', '구분2', '주소']]

df4 = pd.read_excel("영천시_식당_위도경도_구분.xlsx")
df4 = df4.rename(columns={"상호명" : "업소명",
           'Latitude' : "위도",
           "Longitude" : "경도",
           '지번주소': '주소'})
df4 = df4[['업소명', '위도', '경도', '구분1', '구분2', '주소']]

concat_df = pd.concat([df, df2, df3, df4], ignore_index = True)
concat_df['지역'] = '영천'
concat_df.to_excel('영천시_숙소_식당_카페.xlsx', index=False)

os.chdir(r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터")

# 고흥
df = pd.read_excel("고흥_숙박_통합_위도경도_구분.xlsx")
df = df.rename(columns={"소재지전체주소" : "주소",
           'Latitude' : "위도",
           "Longitude" : "경도",
           "사업장명" : "업소명"})
df = df[['업소명', '위도', '경도', '구분1', '구분2', '주소']]


df1 = pd.read_excel("고흥_음식점_위도.경도_구분.xlsx")
df1 = df1.rename(columns={"소재지" : "주소",
           'Latitude' : "위도",
           "Longitude" : "경도"})
df1 = df1[['업소명', '위도', '경도', '구분1', '구분2', '주소']]

concat_df = pd.concat([df, df1], ignore_index = True)
concat_df['지역'] = '고흥'
concat_df.to_excel('고흥시_숙소_식당_카페.xlsx', index=False)

# 문경 
df = pd.read_excel("문경_숙박업소(위도.경도)_구분.xlsx")
df = df.rename(columns={"영업소 주소(도로명)" : "주소",
           'Latitude' : "위도",
           "Longitude" : "경도",
           "사업장명" : "업소명"})
df = df[['업소명', '위도', '경도', '구분1', '구분2', '주소']]

df1 = pd.read_excel("문경_음식점현황_위도경도_구분.xlsx")

df2 = pd.read_excel("문경_카페 현황_위도경도_구분.xlsx")
df2 = df2.rename(columns={"소재지(도로명 주소)" : "주소",
           'Latitude' : "위도",
           "Longitude" : "경도"})
df2 = df2[['업소명', '위도', '경도', '구분1', '구분2', '주소']]

df3 = pd.read_excel("문경_캠핑장_위도.경도_구분.xlsx")
df3 = df3.rename(columns={"펜션명" : "업소명",
           'Latitude' : "위도",
           "Longitude" : "경도",
           "도로명 주소" : "주소"})
df3 = df3[['업소명', '위도', '경도', '구분1', '구분2', '주소']]


concat_df = pd.concat([df, df1, df2, df3], ignore_index = True)
concat_df['지역'] = '문경'
concat_df.to_excel('문경시_숙소_식당_카페.xlsx', index=False)


# 임실
df = pd.read_excel("임실_숙박_통합_위도경도_구분.xlsx")
df = df.rename(columns={"상호명" : "업소명",
           'Latitude' : "위도",
           "Longitude" : "경도"})
df = df[['업소명', '위도', '경도', '구분1', '구분2', '주소']]


df1 = pd.read_excel("임실_음식점 현황_위도경도_구분.xlsx")
df1 = df1.rename(columns={"소재지(도로명)" : "주소",
           'Latitude' : "위도",
           "Longitude" : "경도"})
df1 = df1[['업소명', '위도', '경도', '구분1', '구분2', '주소']]

concat_df = pd.concat([df, df1], ignore_index = True)
concat_df['지역'] = '임실'
concat_df.to_excel('임실군_숙소_식당_카페.xlsx', index=False)




#==============
# 모두 통합
file_list = [
    "임실군_숙소_식당_카페.xlsx",
    "문경시_숙소_식당_카페.xlsx",
    "고흥시_숙소_식당_카페.xlsx",
    "영천시_숙소_식당_카페.xlsx"
]

merged_df = pd.DataFrame()

# 파일 반복 처리
for file in file_list:
    df = pd.read_excel(file)  # 기본 첫 번째 시트만 읽음
    region = file.split('_')[0]  # 파일명에서 지역 추출
    df['지역'] = region
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# 통합된 데이터 저장
merged_df.to_excel("통합_숙소_식당_카페.xlsx", index=False)

# 통합된 기존 숙소/식당/카페 데이터 불러오기
merged_df = pd.read_excel("통합_숙소_식당_카페.xlsx")

# ▶️ 1. 주차장 데이터 불러오기 (주차장 파일명에 맞게 수정 필요)
영천_df = pd.read_excel("영천시_공영주차장_위도경도_구분.xlsx")
임실_df = pd.read_excel("임실_주차장_위도경도.xlsx")
문경_df = pd.read_excel("문경_주차장_위도경도 (1).xlsx")
고흥_df = pd.read_excel("고흥_주차장_위도.경도.xlsx")


# 컬럼 정리: 공통 컬럼 맞추기
영천_df = 영천_df.rename(columns={
    "주차장 명칭": "업소명",  # 또는 "주차장명"
    "Latitude": "위도",
    "Longitude": "경도",
    "도로명(지번) 주소": "주소"
})
영천_df['구분1'] = '주차장'
영천_df['구분2'] = '주차장'

고흥_df = 고흥_df.rename(columns={
    "주차장명": "업소명",  # 또는 "주차장명"
    "위도": "위도",
    "경도": "경도",
    "소재지도로명주소": "주소"
})


문경_df = 문경_df.rename(columns={
    "주차장명": "업소명",  # 또는 "주차장명"
    "Latitude": "위도",
    "Longitude": "경도",
    "주소": "주소"
})


임실_df = 임실_df.rename(columns={
    "주차장명": "업소명",  # 또는 "주차장명"
    "Latitude": "위도",
    "Longitude": "경도",
    "주소": "주소"
})


merged_all = pd.concat([merged_df, 영천_df, 임실_df, 문경_df, 고흥_df], ignore_index=True)
merged_all = merged_all.drop(columns=[col for col in ['업종명', '소재지전화','연번','일반/임시','유형','유/무료','운영','총 주차면 수','일반','확장형',
                                                      '장애인','경차','친환경(전기차)','교통약자','대형','기타','CCTV','충전시설(대수)','주차면수','비고',
                                                      '주차대수','운영시간','평일 요금정보','공휴일 요금정보',
                                                      '기본요금 (기본60분)','시간(분) 당 추가요금','1일주차 추가요금','전화번호','관리기관명',
                                                      '주차장관리번호','주차장구분','주차장유형','소재지지번주소','주차구획수','급지구분','요금정보'] if col in merged_all.columns])
merged_all.to_excel("전체_숙소_식당_카페_주차장_통합.xlsx", index=False)
print("✅ 저장 완료: 전체_숙소_식당_카페_주차장_통합.xlsx")

merged_df = pd.read_excel("전체_숙소_식당_카페_주차장_통합.xlsx")

영천_df = pd.read_excel("영천시__화장실.xlsx")
임실_df = pd.read_excel("임실군_화장실.xlsx")
문경_df = pd.read_excel("문경시_화장실.xlsx")
고흥_df = pd.read_excel("고흥군_화잘실.xlsx")

merged_all = pd.concat([merged_df, 영천_df, 임실_df, 문경_df, 고흥_df], ignore_index=True)
merged_all = merged_all.drop(columns=[col for col in ['번호','구분','근거','소재지지번주소','남성용-대변기수','남성용-소변기수','남성용-장애인용대변기수',
                                                      '남성용-장애인용소변기수','남성용-어린이용대변기수','남성용-어린이용소변기수','여성용-대변기수',
                                                      '여성용-장애인용대변기수','여성용-어린이용대변기수','관리기관명','전화번호','개방시간','개방시간상세',
                                                      '설치연월','화장실소유구분','오물처리방식','안전관리시설설치대상여부','비상벨설치여부','비상벨설치장소','화장실입구CCTV설치유무',
                                                      '기저귀교환대유무','기저귀교환대장소','리모델링연월','데이터기준일자'] if col in merged_all.columns])
merged_all.to_excel("전체_숙소_식당_카페_주차장_화장실_통합.xlsx", index=False)
print("✅ 저장 완료: 전체_숙소_식당_카페_주차장_화장실_통합.xlsx")







import pandas as pd

# 파일 경로
input_path = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\최종_숙소_식당_주차장_화장실(최종_축제명)0.xlsx"


# 엑셀 파일 읽기
df = pd.read_excel(input_path)

# 세미콜론 기준으로 축제명을 나누고 행을 늘림
df_split = df.assign(축제명=df['축제명'].str.split(';')).explode('축제명')

# 공백 제거 (필요 시)
df_split['축제명'] = df_split['축제명'].str.strip()

# 저장
output_path = "최종_인프라_축제명_행으로분리.xlsx"
df_split.to_excel(output_path, index=False)





















import pandas as pd

# 1. 파일 불러오기
input_path = "최종_숙소_식당_주차장-화장실(축제명)_분리.xlsx"
df = pd.read_excel(input_path)

# 2. 작약꽃축제 A/B/C → 작약꽃축제로 통합
df["축제명"] = df["축제명"].replace({
    "작약꽃축제A": "작약꽃축제",
    "작약꽃축제B": "작약꽃축제",
    "작약꽃축제C": "작약꽃축제"
})

# 3. 중복 제거: 위도, 경도, 업소명, 축제명 기준 (필요시 컬럼 조정 가능)
dedup_df = df.drop_duplicates(subset=["업소명", "위도", "경도", "구분1", "축제명"])

# 4. 저장
output_path = "최종_숙소_식당_주차장-화장실(축제명)_중복제거_작약통합.xlsx"
dedup_df.to_excel(output_path, index=False)

print(f"✅ 저장 완료: {output_path}")










































############
# 인프라 요약표 / 인프라 막대그래프용 파일 생성
import pandas as pd
from geopy.distance import geodesic

# 파일 경로
infra_raw_path = "../3/3조_프로젝트_data/영천시_숙소_식당_카페(축제명).xlsx"
info_path = "../3/3조_프로젝트_data/축제정보.xlsx"

# 데이터 불러오기
df_infra = pd.read_excel(infra_raw_path)
df_info = pd.read_excel(info_path)

# 중심 좌표 계산 (축제별 평균 위도/경도)
festival_centers = df_info.groupby("축제명")[["위도", "경도"]].mean().to_dict(orient="index")

# 위도, 경도 결측 제거
df_infra_clean = df_infra.dropna(subset=["위도", "경도"])

# 인프라 요약표 생성
infra_summary = []

for fest, center in festival_centers.items():
    lat_center, lon_center = center["위도"], center["경도"]
    df_sub = df_infra_clean[df_infra_clean["축제명"] == fest].copy()

    # 거리 계산
    distances = [
        geodesic((lat_center, lon_center), (row["위도"], row["경도"])).km
        for _, row in df_sub.iterrows()
    ]
    df_sub["거리"] = distances
    df_within_10km = df_sub[df_sub["거리"] <= 10]

    숙소수 = df_within_10km[df_within_10km["구분1"] == "숙소"].shape[0]
    식당수 = df_within_10km[df_within_10km["구분1"] == "식당"].shape[0]
    비율 = round(숙소수 / 식당수, 2) if 식당수 != 0 else None

    infra_summary.append({
        "축제명": fest,
        "숙소 수(10km)": 숙소수,
        "음식점 수(10km)": 식당수,
        "숙소/음식점 비율": 비율
    })

df_infra_summary = pd.DataFrame(infra_summary)

# 그래프용 데이터: 긴 형태로 변환
df_bar_long = pd.melt(
    df_infra_summary,
    id_vars=["축제명"],
    value_vars=["숙소 수(10km)", "음식점 수(10km)"],
    var_name="업소유형",
    value_name="업소수"
)
df_bar_long["업소유형"] = df_bar_long["업소유형"].map({
    "숙소 수(10km)": "숙소",
    "음식점 수(10km)": "식당"
})

# 저장
infra_summary_path = "../3/3조_프로젝트_data/인프라요약_전처리결과.xlsx"
bar_data_path = "../3/3조_프로젝트_data/인프라그래프데이터_전처리결과.xlsx"

df_infra_summary.to_excel(infra_summary_path, index=False)
df_bar_long.to_excel(bar_data_path, index=False)

infra_summary_path, bar_data_path



# <아래 코드 돌리면 각 축제별 html파일 생성됨>

import pandas as pd
import folium
from folium import FeatureGroup
import json
import os

# ======== 파일 경로 ========
festival_file = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\축제정보.xlsx"
infra_file = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\최종_숙소_식당_주차장_화장실(최종_축제명).xlsx"
geojson_path = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\a.geojson"

# ======== 데이터 로드 ========
df_festival = pd.read_excel(festival_file)
df_place = pd.read_excel(infra_file)

# ======== GeoJSON 로드 ========
with open(geojson_path, encoding="utf-8") as f:
    yc_geojson = json.load(f)

# ======== 축제 그룹 설정 ========
festival_groups = {
    "작약꽃축제": ["작약꽃축제A", "작약꽃축제B", "작약꽃축제C"],
    "와인페스타": ["와인페스타"],
    "별빛축제": ["별빛축제"],
    "벚꽃축제": ["옥정호 벚꽃축제"],
    "오미자축제": ["오미자축제"],
    "우주항공축제": ["우주항공축제"],
}

# ======== 영천 관련 축제만 경계 표시 ========
festivals_in_yc = {"작약꽃축제", "와인페스타", "별빛축제"}

# ======== 색상 매핑 ========
color_map = {"숙소": "red", "식당": "green", "화장실": "orange", "주차장": "blue"}

# ======== 저장 경로 리스트 ========
saved_paths = []

# ======== 축제별 지도 생성 ========
for file_label, fests in festival_groups.items():
    df_fests = df_festival[df_festival["축제명"].isin(fests)]

    # 지도 중심 좌표 계산
    center_lat = df_fests["위도"].mean()
    center_lon = df_fests["경도"].mean()

    # 지도 생성
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="CartoDB positron")

    # ======== 영천시 경계 표시 여부 ========
    if file_label in festivals_in_yc:
        folium.GeoJson(
            yc_geojson,
            name="영천시 경계",
            style_function=lambda x: {
                "color": "gray",
                "weight": 2,
                "fillOpacity": 0
            }
        ).add_to(m)

    # ======== 전체 인프라 표시 ========
    for category in df_place["구분1"].dropna().unique():
        fg = FeatureGroup(name=category, show=True)
        df_cat = df_place[df_place["구분1"] == category]
        for _, row in df_cat.iterrows():
            lat, lon = row["위도"], row["경도"]
            if pd.notnull(lat) and pd.notnull(lon):
                folium.CircleMarker(
                    location=(lat, lon),
                    radius=3,
                    color=color_map.get(category, "gray"),
                    fill=True,
                    fill_opacity=0.7,
                    popup=f"{category}: {row['업소명']}"
                ).add_to(fg)
        fg.add_to(m)

    # ======== 축제 마커 및 반경 표시 ========
    for _, row in df_fests.iterrows():
        lat, lon = row["위도"], row["경도"]
        if pd.notnull(lat) and pd.notnull(lon):
            popup_text = f"<b>{row['축제명']}</b><br>개최시기: {row['개최시기(월)']}월<br>일일 평균 방문객: {round(row['일일방문객(명)']):,}명"
            folium.Marker(
                location=(lat, lon),
                icon=folium.Icon(color='blue', icon='info-sign'),
                popup=popup_text
            ).add_to(m)
            folium.Circle(
                radius=10000,  # 시각적 반경 강조용
                location=(lat, lon),
                color='blue',
                fill=True,
                fill_opacity=0.05
            ).add_to(m)

    # 레이어 컨트롤 추가
    folium.LayerControl(collapsed=False).add_to(m)

    # 저장
    file_safe = file_label.replace(" ", "_")
    output_path = f"{file_safe}_축제_인프라_지도_전체표시.html"
    m.save(output_path)
    saved_paths.append(os.path.abspath(output_path))

# ======== 결과 출력 ========
print("생성된 파일 목록:")
for path in saved_paths:
    print(path)




# < 작약꽃축제 html만드는 코드>

import pandas as pd
import folium
from folium import FeatureGroup
import json
import numpy as np

# 기본 정보
merged_fests = ["작약꽃축제A", "작약꽃축제B", "작약꽃축제C"]
df_festivals = df_festival[df_festival["축제명"].isin(merged_fests)]

# 지도 중심
center_lat = df_festivals["위도"].mean()
center_lon = df_festivals["경도"].mean()

# 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="CartoDB positron")

# GeoJSON 경계 추가
folium.GeoJson(
    yc_geojson,
    name="영천시 경계",
    style_function=lambda x: {
        "color": "gray",
        "weight": 2,
        "fillOpacity": 0
    }
).add_to(m)

# 색상 매핑
color_map = {"숙소": "red", "식당": "green", "화장실": "orange", "주차장": "blue"}

# === 전체 인프라 표시 ===
for category in df_place["구분1"].dropna().unique():
    fg = FeatureGroup(name=category, show=True)
    df_cat = df_place[df_place["구분1"] == category]
    for _, row in df_cat.iterrows():
        lat, lon = row["위도"], row["경도"]
        if pd.notnull(lat) and pd.notnull(lon):
            folium.CircleMarker(
                location=(lat, lon),
                radius=3,
                color=color_map.get(category, "gray"),
                fill=True,
                fill_opacity=0.7,
                popup=f"{category}: {row['업소명']}"
            ).add_to(fg)
    fg.add_to(m)

# === 축제별 필터 레이어 추가 ===
for fest in merged_fests:
    df_sub = df_festivals[df_festivals["축제명"] == fest]
    fg = FeatureGroup(name=f"🎉 {fest}", show=True)
    for _, row in df_sub.iterrows():
        lat, lon = row["위도"], row["경도"]
        if pd.notnull(lat) and pd.notnull(lon):
            popup_text = f"<b>{row['축제명']}</b><br>개최시기: {row['개최시기(월)']}월<br>일일 평균 방문객: {round(row['일일방문객(명)']):,}명"
            folium.Marker(
                location=(lat, lon),
                icon=folium.Icon(color='blue', icon='info-sign'),
                popup=popup_text
            ).add_to(fg)
            folium.Circle(
                radius=10000,  # 시각적 강조용
                location=(lat, lon),
                color='blue',
                fill=True,
                fill_opacity=0.05
            ).add_to(fg)
    fg.add_to(m)

# 레이어 컨트롤
folium.LayerControl(collapsed=False).add_to(m)

# 저장
final_path = r"C:\Users\USER\Documents\lsbigdata-gen4\project4\3조_프로젝트_data\모든 데이터\작약꽃축제_축제_인프라_지도_전체표시.html"
m.save(final_path)

final_path

