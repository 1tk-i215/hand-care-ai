import streamlit as st
import joblib
import numpy as np
from pathlib import Path
MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"
model = joblib.load(MODEL_PATH)
from PIL import Image
import time

st.set_page_config(page_title="Hand Care AI",page_icon="👊",layout="centered")
st.markdown("""
<style>

/* 左側のサイドバー */
[data-testid="stSidebar"] {
    background-color: #e5f4f8;
}

/* サイドバーの文字色 */
[data-testid="siSidebar"] * {
    color: #526875;
}

/* ページ全体 */

.stApp {
    background-color: #fff8fa;
}

/* メインタイトル *
/h1 {
    text-align: center;
    color: #c77d8a;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

    /* 説明文 :/
 h3 {
    text-align: center;
    color: #8f6870;
}

/* アップロード部分 */
[data-testid="stFileUploader"]{
    background-color: #ffffff;
    border: 2px dashed #e7a9b4;
    border-radius: 20px;
    padding: 25px;
    margin-top: 20px;
}

/* アップロード部分の文字 */
[data-testid="stFileUploader"] section {
    background-color: #fffafb
    border-radius: 15px;
} 

/* サイドバー*/
[data-testid="stSidebar"] p {
    color: #76545c;
}

/* 区切り線 */
hr {
    border-color: #f0cbd1;
}

/* 診断結果 */
[data-testid="stAlert"] {
    border-radious: 15px
}

/* ボタン */
button {
    border-radius: 12px !important;
}
/* 文字を濃くして見やすくする */
[data-testid="stMarkdownContainer"] * {
    color: #4a3a3d; !important;
}

/* 診断結果 */
[data-testid="stAlert"] * {
    color: #4a3a3d; !impportant;
}

/* おすすめカード */
.recommend-card {
    background-color: #fff0f4;
    border-radius: 20px;
    padding: 25px;
    margin-top: 20px
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(180,130,140,0.25);
    border: 2px solid #e7a9b4;
}

.recommend-title {
    color: #8f6870;
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 12px;
}

.recommend-product {
    color: #4a3a3d;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 8px;
}

.recommend-text {
    color: 36b5559;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True
)

st.sidebar.title("👊　Hand Care AI")

st.sidebar.write("使い方")
st.sidebar.write("①　手の写真を選ぶ")
st.sidebar.write("②　診断する")
st.sidebar.write("③　結果を見る")


st.title("👊　Hand Care AI")

st.markdown(
  "<h3>あなたの手肌に合うハンドクリームを見つけよう</h3>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#a47b83;'>"
    "手の写真から乾燥状態や赤みをチェックします"
    "</p>",
    unsafe_allow_html=True
)
st.divider()

uploaded_file = st.file_uploader(
    "📷 手の写真を選択してください",
    type=["jpg","jpeg","png"]
    )
if uploaded_file is not None:
    img = Image.open(uploaded_file)

    st.image(img, caption="📷　診断する手の画像", width=350)

    with st.spinner("🔍　手の状態を解析中…"):
        time.sleep(2)
        st.success("☑　診断が完了しました！")

    gray = img.convert("L")

    pixels = list(gray.getdata())

    average = sum(pixels)/len(pixels)

    variance = sum((p - average)**2 for p in pixels)/len(pixels)

    img=img.convert("RGB")
    
    pixels=list(img.getdata())
    
    red_avg = sum(pixel[0] for pixel in pixels)/len(pixels)
    green_avg = sum(pixel[1] for pixel in pixels)/len(pixels)
    blue_avg = sum(pixel[2] for pixel in pixels)/len(pixels)
    if  red_avg > green_avg + 10:
        redness = "あり"
    else:
        redness = "なし"
    st.info(f"赤み:{redness}")

    st.write("－－－－－判定結果－－－－－")

    img_ai = img.convert("RGB").resize((64,64))
    pixels_ai = np.array(img_ai).flatten().reshape(1,-1)

    prediction = model.predict(pixels_ai)[0]
    dryness = int(prediction)

    st.write("乾燥度:", dryness)

    if red_avg > green_avg + 10:
     redness = "あり"
    else:
     redness = "なし"
    st.info(f"赤み:{redness}")

    if dryness == "5":
     star = "★★★★★"
     st.subheader("🧴　おすすめ: 乾燥肌向けハンドクリーム")
     st.success("アトリックス　薬用ハンドクリーム UR <L>")
     st.write("はちみつ配合で高い保湿力があります")

    elif dryness == "4" and redness == "あり":
     star = "★★★★☆"
     st.subheader("🧴　おすすめ: 敏感肌向けハンドクリーム")
     st.success("ユースキン A")         
     st.write("")

    elif dryness == "3" and redness == "あり":
     star = "★★★☆☆"
     st.subheader("🧴　おすすめ: 敏感肌向けハンドクリーム")
     st.success("カルテHD　モイスチュアハンドクリーム")
     st.write("セラミド配合で敏感肌に優しい")

    elif dryness == 2:
     star = "★★☆☆☆"
     st.subheader("🧴　おすすめ: 敏感肌向けハンドクリーム")
     st.success("メンソレータムハンドベール しっとりクリーム")
     st.write("しっとり")
     
    elif dryness == 1:
     star = "★☆☆☆☆"
     st.subheader("🧴　おすすめ: 軽い使用感のハンドクリーム")
     st.success("アトリックス ビューティーチャージ")
     st.write("保湿・滑らかさの維持に向いている")

     st.write("### ⭐ 乾燥レベル")

if "star" not in locals( ):
    star = ""

st.write(star)

