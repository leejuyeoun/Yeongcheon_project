from pathlib import Path
import pandas as pd

app_dir = Path(__file__).parent

df_info = pd.read_excel(app_dir / "축제정보.xlsx")
df_compare = pd.read_excel(app_dir / "축제비교대상선정이유.xlsx")
df_infra_summary = pd.read_excel(app_dir / "최종_인프라요약_전처리결과.xlsx")
df_bar_long = pd.read_excel(app_dir / "최종_인프라그래프데이터_전처리결과.xlsx")
df_infra_combined = pd.read_excel(app_dir / "최종_숙소_식당_주차장_화장실.xlsx")
df_stats = pd.read_excel(app_dir / "최종_숙소_식당_주차장_화장실(축제명)_분리.xlsx")
df_infra_merged = pd.read_excel(app_dir / "최종_숙소_식당_주차장_화장실(축제명).xlsx")