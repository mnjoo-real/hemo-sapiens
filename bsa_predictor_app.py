import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# --- CSV 흡광도 파일에서 595nm 추출 함수 ---
def extract_abs_at_595(csv_path):
    df = pd.read_csv(csv_path)
    df_filtered = df[(df['nm'] >= 400) & (df['nm'] <= 700)]
    if 595 in df_filtered['nm'].values:
        return df_filtered[df_filtered['nm'] == 595]['Abs'].values[0]
    else:
        return df_filtered.iloc[(df_filtered['nm'] - 595).abs().argmin()]['Abs']

# --- 빛 반사 최소 영역 RGB 추출 함수 ---
def extract_smallest_uniform_rgb(img: Image.Image, min_crop_size=10):
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
    return np.mean(best_rgb_crop.reshape(-1, 3), axis=0)

# --- RGB to Absorbance Polynomial Regression Model (Refined RGB) ---
rgb_data = np.array([
    [53.9776202, 73.6837004, 76.7938818],   # BSA 15
    [41.2205387, 69.1725234, 83.3591872],   # BSA 22.5
    [16.5844049, 57.9971645, 88.7071514],   # BSA 30
    [13.3263845, 45.5699462, 82.0763522]    # BSA 37.5
])
absorbance_values = [0.336979, 0.345618, 0.383324, 0.578829]

# Use 2nd-degree polynomial regression
poly_model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
poly_model.fit(rgb_data, absorbance_values)

# --- Absorbance to Concentration Conversion ---
slope = 73.985
intercept = -4.172

def predict_absorbance(rgb):
    return poly_model.predict([rgb])[0]

def predict_concentration(abs_val):
    return slope * abs_val + intercept

# --- Streamlit App ---
st.title("🧪 BSA 농도 예측기")
st.write("용액의 RGB 값으로 농도를 예측합니다.")

uploaded_file = st.file_uploader("📷 이미지 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_column_width=True)

    avg_rgb = extract_smallest_uniform_rgb(image)
    predicted_abs = predict_absorbance(avg_rgb)
    predicted_conc = predict_concentration(predicted_abs)

    st.markdown("---")
    st.subheader("🎯 예측 결과")
    st.write(f"**RGB 평균값:** R={avg_rgb[0]:.2f}, G={avg_rgb[1]:.2f}, B={avg_rgb[2]:.2f}")
    #st.write(f"**예측된 흡광도:** {predicted_abs:.4f}")
    st.write(f"**예측된 농도:** {predicted_conc:.2f} µg/mL")

# --- Absorbance CSV Plotting ---
# st.markdown("---")
# st.subheader("📊 흡광도 스펙트럼 시각화")
# csv_file = st.file_uploader("📄 흡광도 CSV 업로드 (nm vs Abs)", type=["csv"], key="csv")

# if csv_file:
#     try:
#         df = pd.read_csv(csv_file)
#         df = df[(df['nm'] >= 400) & (df['nm'] <= 700)]
#         if 'nm' in df.columns and 'Abs' in df.columns:
#             st.line_chart(df.set_index('nm'))
#             abs_595 = extract_abs_at_595(csv_file)
#             st.success(f"🔬 595nm에서의 흡광도: {abs_595:.4f}")
#         else:
#             st.error("CSV 파일에 'nm'과 'Abs' 열이 포함되어야 합니다.")
#     except Exception as e:
#         st.error(f"CSV 파일을 불러오는 중 오류가 발생했습니다: {e}")