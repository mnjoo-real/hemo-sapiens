import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정 (Windows의 경우 'Malgun Gothic' 사용)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 파일 경로 설정
file_paths = {
    "0.05 (10min)": r"dataset\이채원\이채원_1.csv",
    "0.1 (10min)": r"dataset\이채원\이채원_2.csv",
    "0.2 (10min)": r"dataset\이채원\이채원_3.csv",
    "0.5 (10min)": r"dataset\이채원\이채원_4.csv",
    "0.05 (20min)": r"dataset\이채원\이채원2_1.csv",
    "0.1 (20min)": r"dataset\이채원\이채원2_2.csv",
    "0.2 (20min)": r"dataset\이채원\이채원2_3.csv",
    "0.5 (20min)": r"dataset\이채원\이채원2_4.csv",
}

# 파장 필터 범위
min_nm, max_nm = 250, 700

# 그래프 초기 설정
plt.figure(figsize=(12, 8))

# 파일별로 선형 그래프 그리기
for label, path in file_paths.items():
    df = pd.read_csv(path)
    nm = df.iloc[:, 0]
    abs_val = df.iloc[:, 1]
    mask = (nm >= min_nm) & (nm <= max_nm)
    # 색상 지정: 10min은 파란색, 20min은 빨간색
    if "10min" in label:
        color = 'blue'
    elif "20min" in label:
        color = 'red'
    else:
        color = 'black'
    plt.plot(nm[mask], abs_val[mask], label=label, color=color)

# 그래프 설정
plt.title(f"ALP Concentration vs Absorbance ({min_nm}–{max_nm} nm)")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance")
plt.legend()
plt.grid(True)
plt.tight_layout()

# 왼쪽(세로축) 숫자 제거
plt.yticks([])

plt.show()