import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정 (Windows의 경우 'Malgun Gothic' 사용)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 파일 경로 설정
file_paths = {
    "저단백": r"dataset\이아윤\BSA_15.csv",
    "저단백 경계": r"dataset\이아윤\BSA_22.5.csv",
    "고단백 경계": r"dataset\이아윤\BSA_30.csv",
    "고단백": r"dataset\이아윤\BSA_37.5.csv",
    "혈액": r"dataset\이아윤\TPV.csv"
}

# 파장 필터 범위
min_nm, max_nm = 400, 900

# 그래프 초기 설정
plt.figure(figsize=(12, 8))

# 파일별로 선형 그래프 그리기
for label, path in file_paths.items():
    df = pd.read_csv(path)
    nm = df.iloc[:, 0]
    abs_val = df.iloc[:, 1]
    mask = (nm >= min_nm) & (nm <= max_nm)
    # 색상 지정: Human blood는 빨간색, 나머지는 파란색
    color = 'red' if label == "혈액" else 'blue'
    plt.plot(nm[mask], abs_val[mask], label=label, color=color)

# 그래프 설정
plt.title(f"BSA Concentration vs Absorbance ({min_nm}–{max_nm} nm)")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
