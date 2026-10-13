import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows의 경우 'Malgun Gothic' 사용)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 💡 보정식 정의: 농도 = 73.985 * 흡광도 - 4.172
def linear_fit(absorbance):
    return 73.985 * absorbance - 4.172

# 📌 예측용 흡광도 범위 (예: 0.3 ~ 0.6)
abs_range = np.linspace(0.3, 0.6, 100)
concentration_pred = linear_fit(abs_range)

# 🔴 실험 측정값들 (흡광도 → 농도)
measured_abs = np.array([0.336979, 0.345618, 0.383324, 0.578829])
measured_conc = linear_fit(measured_abs)

# 📊 그래프 그리기
plt.figure(figsize=(6, 4))
plt.plot(abs_range, concentration_pred, label='선형 보정식', color='blue')
plt.scatter(measured_abs, measured_conc, color='red', label='실험값')
plt.title("흡광도(595nm)와 BSA 농도 간의 선형 관계")
plt.xlabel("흡광도 (Abs at 595nm)")
plt.ylabel("농도 (μg/mL)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
