import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# --- RGB 추출 + 시각화 함수 ---
def extract_smallest_uniform_rgb_with_box(img: Image.Image, min_crop_size=10):
    img = img.convert("RGB")
    np_img = np.array(img)
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape
    best_std = float('inf')
    best_crop = None
    crop_sizes = range(min_crop_size, min(h, w) // 2, 5)

    for crop_size in crop_sizes:
        for y in range(0, h - crop_size, 5):
            for x in range(0, w - crop_size, 5):
                window = gray[y:y+crop_size, x:x+crop_size]
                std = np.std(window)
                if std < best_std:
                    best_std = std
                    best_crop = (x, y, crop_size, crop_size)

    x, y, cw, ch = best_crop
    best_rgb_crop = np_img[y:y+ch, x:x+cw]
    avg_rgb = np.mean(best_rgb_crop.reshape(-1, 3), axis=0)

    # 사각형 표시 이미지
    img_with_box = np_img.copy()
    cv2.rectangle(img_with_box, (x, y), (x+cw, y+ch), (255, 0, 0), 2)
    return avg_rgb, img_with_box

# --- 회귀 모델 학습 ---
rgb_data = np.array([
    [53.9776202, 73.6837004, 76.7938818],   # BSA 15
    [41.2205387, 69.1725234, 83.3591872],   # BSA 22.5
    [16.5844049, 57.9971645, 88.7071514],   # BSA 30
    [13.3263845, 45.5699462, 82.0763522]    # BSA 37.5
])
absorbance_values = [0.336979, 0.345618, 0.383324, 0.578829]

model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(rgb_data, absorbance_values)

def predict_abs(rgb): return model.predict([rgb])[0]
def abs_to_conc(abs_val): return 73.985 * abs_val - 4.172

# --- Streamlit 앱 시작 ---
st.title("🧪 BSA 농도 예측기")
st.write("well 이미지의 색상만으로 BSA 농도를 예측합니다.")

uploaded_file = st.file_uploader("📷 이미지 업로드", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    avg_rgb, image_with_box = extract_smallest_uniform_rgb_with_box(image)
    predicted_abs = predict_abs(avg_rgb)
    predicted_conc = abs_to_conc(predicted_abs)
    rgb_hex = "#{:02x}{:02x}{:02x}".format(int(avg_rgb[0]), int(avg_rgb[1]), int(avg_rgb[2]))

    # --- 이미지 한 줄 표시 ---
    st.subheader("🎯 예측 결과")
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="업로드된 이미지", width=250)
    with col2:
        st.image(image_with_box, caption="RGB 추출 영역 (파란 사각형)", width=250)

    st.write(f"**RGB 평균값:** R={avg_rgb[0]:.2f}, G={avg_rgb[1]:.2f}, B={avg_rgb[2]:.2f}")
    st.markdown(
        f"<div style='width: 100px; height: 50px; background-color: {rgb_hex}; border: 1px solid #000'></div>",
        unsafe_allow_html=True
    )
    st.write(f"**예측된 농도:** {predicted_conc:.2f} µg/mL")

    # --- 실제 흡광도 vs 예측 흡광도 ---
    st.markdown("### 📊 실제 흡광도 vs 예측 흡광도")
    preds = model.predict(rgb_data)
    names = ['15', '22.5', '30', '37.5']

    fig1, ax1 = plt.subplots()
    ax1.scatter(absorbance_values, preds, color='blue', label='학습 예측값')
    ax1.plot(absorbance_values, absorbance_values, 'r--', label='표준 곡선')
    for i, name in enumerate(names):
        ax1.text(absorbance_values[i], preds[i], f"BSA {name}")
    ax1.scatter([predicted_abs], [predicted_abs], color='red', s=100, label='업로드 이미지 예측값', zorder=5)
    ax1.set_xlabel("실제 흡광도")
    ax1.set_ylabel("예측 흡광도")
    ax1.set_title("실제 vs 예측 흡광도")
    ax1.legend()
    st.pyplot(fig1)

    # --- 실제 농도 vs 예측 농도 ---
    st.markdown("### 📊 실제 농도 vs 예측 농도")
    true_concs = np.array([15, 22.5, 30, 37.5])
    predicted_concs = [abs_to_conc(a) for a in absorbance_values]

    fig2, ax2 = plt.subplots()
    ax2.scatter(true_concs, predicted_concs, color='blue', label='학습 예측값')
    ax2.plot(true_concs, true_concs, 'r--', label='표준 곡선')
    for i, val in enumerate(true_concs):
        ax2.text(true_concs[i], predicted_concs[i], f"{val}")
    ax2.scatter([predicted_conc], [predicted_conc], color='red', s=100, label='업로드 이미지 예측값', zorder=5)
    ax2.set_xlabel("실제 농도 (µg/mL)")
    ax2.set_ylabel("예측 농도 (µg/mL)")
    ax2.set_title("실제 농도 vs 예측 농도")
    ax2.legend()
    st.pyplot(fig2)

    # --- 흡광도 vs 농도 ---
    st.markdown("### 📊 흡광도 vs 농도 관계")

    fig3, ax3 = plt.subplots()
    ax3.scatter(absorbance_values, true_concs, color='blue', label='학습 데이터')
    abs_range = np.linspace(min(absorbance_values)-0.02, max(absorbance_values)+0.02, 100)
    conc_range = abs_to_conc(abs_range)
    ax3.plot(abs_range, conc_range, 'green', linestyle='--', label='흡광도→농도 회귀선')
    ax3.scatter([predicted_abs], [predicted_conc], color='red', s=100, label='업로드 이미지 예측값', zorder=5)
    for i, abs_val in enumerate(absorbance_values):
        ax3.text(abs_val, true_concs[i], f"{true_concs[i]} µg/mL")
    ax3.set_xlabel("흡광도 (Abs at 595nm)")
    ax3.set_ylabel("실제 농도 (µg/mL)")
    ax3.set_title("흡광도 vs 농도 관계")
    ax3.legend()
    st.pyplot(fig3)
