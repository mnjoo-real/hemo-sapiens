import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로와 레이블 정의
seyoung_files = {
    "40(μg/mL)": r"dataset\전세영\seyoung40.csv",
    "80(μg/mL)": r"dataset\전세영\seyoung80.csv",
    "120(μg/mL)": r"dataset\전세영\seyoung120.csv",
    "160(μg/mL)": r"dataset\전세영\seyoung160.csv",
    "200(μg/mL)": r"dataset\전세영\seyoung200.csv",
    "240(μg/mL)": r"dataset\전세영\seyoung240.csv",
}

# 그래프 그리기
plt.figure(figsize=(12, 8))

for label, path in seyoung_files.items():
    df = pd.read_csv(path)
    nm = df.iloc[:, 0]        # 첫 번째 열: 파장 (nm)
    abs_val = df.iloc[:, 1]   # 두 번째 열: 흡광도 (Absorbance)
    mask = (nm >= 400) & (nm <= 900)  # 400~900nm 범위만 선택
    plt.plot(nm[mask], abs_val[mask], label=label)

# 그래프 설정
plt.title("Ammonia Concentration vs Absorbance (400–900 nm)")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance")
plt.ylim(-0.2, 0.6)  # 세로축(흡광도) 범위 설정
plt.legend(title="Concentration")
plt.grid(True)
plt.tight_layout()
plt.show()