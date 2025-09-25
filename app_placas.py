import streamlit as st
import cv2
import pytesseract
import numpy as np
import tempfile
import os

st.set_page_config(page_title="Reconocimiento de Placas", layout="centered")

st.title("📷 Reconocimiento de Placas Vehiculares (Formato Peruano)")
st.write("Sube imágenes de placas vehiculares y genera un archivo `.txt` con las placas reconocidas automáticamente.")

with st.expander("📸 Recomendaciones para tomar fotos"):
    st.markdown("""
    - La placa debe estar **centrada y completamente visible**.
    - Evita **sombras, reflejos o desenfoques**.
    - Usa **buena iluminación**, preferiblemente de día.
    - Usa **resolución alta**.
    - Toma la foto lo más **perpendicular posible** a la placa.
    """)

uploaded_files = st.file_uploader("Sube una o más imágenes de placas", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

def extract_plate_text(image_bytes):
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 11, 17, 17)
    text = pytesseract.image_to_string(filtered, config='--psm 8')
    return text.strip().replace("\n", "").replace(" ", "")

plate_texts = []

if uploaded_files:
    st.subheader("🔍 Resultados del reconocimiento")
    for file in uploaded_files:
        plate = extract_plate_text(file.read())
        if plate:
            plate_texts.append(plate)
            st.write(f"📄 {file.name}: `{plate}`")
        else:
            st.write(f"📄 {file.name}: ❌ No se pudo reconocer la placa")

    if plate_texts:
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as f:
            for plate in plate_texts:
                f.write(plate + "\n")
            temp_file_path = f.name

        with open(temp_file_path, "rb") as f:
            st.download_button("📥 Descargar archivo de placas reconocidas", f, file_name="placas_reconocidas.txt", mime="text/plain")
