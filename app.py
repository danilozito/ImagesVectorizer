import streamlit as st
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64
from main import preprocess_image, bitmap_to_potrace, generate_svg, process_image

# Configurazione della pagina
st.set_page_config(
    page_title="Convertitore Immagini in SVG",
    page_icon="🖼️",
    layout="wide"
)

# Titolo dell'app
st.title("Convertitore di Immagini in SVG")
st.markdown("Carica un'immagine e convertila in formato SVG vettoriale")

# Sidebar per i parametri
st.sidebar.header("Parametri di Conversione")

# Aggiungo una spiegazione dei parametri
st.sidebar.markdown("""
### Legenda dei parametri:

**Soglia di binarizzazione**: 
Determina quali pixel diventano bianchi o neri. 
- Valori più bassi: più dettagli ma più rumore
- Valori più alti: meno dettagli ma più pulito

**Dimensione kernel sfocatura**: 
Controlla quanto viene sfocata l'immagine prima della conversione.
- Valori più bassi: mantiene più dettagli fini
- Valori più alti: rimuove più rumore ma può perdere dettagli
""")

threshold = st.sidebar.slider("Soglia di binarizzazione", 0, 255, 100, 5)
blur = st.sidebar.slider("Dimensione kernel sfocatura", 1, 21, 5, 2)

# Funzione per visualizzare l'SVG
def display_svg(svg_path):
    with open(svg_path, "r") as f:
        svg_content = f.read()
    
    # Codifica l'SVG in base64 per visualizzarlo
    b64 = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" width="100%"/>'
    return html

# Funzione per salvare l'immagine temporanea
def save_temp_image(image, filename="temp_image"):
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    img_path = os.path.join("temp", f"{filename}")
    cv2.imwrite(img_path, image)
    return img_path

# Funzione per convertire l'immagine
def convert_image(uploaded_file, threshold, blur):
    # Crea cartella temporanea se non esiste
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # Salva l'immagine caricata
    input_path = os.path.join("temp", uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Genera il percorso di output
    file_name = os.path.splitext(uploaded_file.name)[0]
    output_path = os.path.join("temp", f"{file_name}.svg")
    
    # Processa l'immagine
    process_image(input_path, output_path, threshold, blur, False)
    
    # Ottieni l'immagine binaria per l'anteprima
    binary = preprocess_image(input_path, threshold, blur)
    
    return input_path, output_path, binary

# Area per caricare l'immagine
uploaded_file = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png", "bmp", "webp", "gif"])

if uploaded_file is not None:
    # Mostra l'immagine originale
    image = Image.open(uploaded_file)
    
    # Ottieni il nome del file per il download
    file_name = os.path.splitext(uploaded_file.name)[0]
    
    # Converti l'immagine
    with st.spinner("Conversione in corso..."):
        input_path, output_path, binary = convert_image(uploaded_file, threshold, blur)
    
    # Mostra i risultati in tre colonne
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Immagine Originale")
        st.image(image, use_container_width=True)
    
    with col2:
        st.subheader("Immagine Binaria")
        st.image(binary, use_container_width=True)
    
    with col3:
        st.subheader("Risultato SVG")
        st.markdown(display_svg(output_path), unsafe_allow_html=True)
    
    # Pulsante per scaricare l'SVG
    with open(output_path, "r") as f:
        svg_content = f.read()
    
    st.download_button(
        label="Scarica SVG",
        data=svg_content,
        file_name=f"{file_name}.svg",
        mime="image/svg+xml"
    )

# Batch conversion section
st.markdown("---")
st.header("Conversione Batch")
st.markdown("Converti tutte le immagini dalla cartella 'Images/ToConvert' a 'Images/Converted'")

if st.button("Converti Tutte le Immagini"):
    # Crea le cartelle se non esistono
    input_dir = os.path.join("Images", "ToConvert")
    output_dir = os.path.join("Images", "Converted")
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        st.info(f"Creata cartella {input_dir}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        st.info(f"Creata cartella {output_dir}")
    
    # Ottieni la lista di tutti i file nella cartella di input
    image_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and 
                  f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp'))]
    
    if not image_files:
        st.warning(f"Nessuna immagine trovata in {input_dir}")
    else:
        st.info(f"Trovate {len(image_files)} immagini da convertire...")
        
        # Crea una barra di progresso
        progress_bar = st.progress(0)
        
        # Converti ogni immagine
        for i, img_file in enumerate(image_files):
            input_path = os.path.join(input_dir, img_file)
            file_name = os.path.splitext(img_file)[0]
            output_path = os.path.join(output_dir, f"{file_name}.svg")
            
            st.text(f"Conversione di {img_file}...")
            try:
                process_image(input_path, output_path, threshold, blur, False)
                st.success(f"Convertito: {img_file} -> {file_name}.svg")
            except Exception as e:
                st.error(f"Errore durante la conversione di {img_file}: {str(e)}")
            
            # Aggiorna la barra di progresso
            progress_bar.progress((i + 1) / len(image_files))
        
        st.success(f"Conversione completata. I file SVG sono stati salvati in {output_dir}")

# Footer
st.markdown("---")
st.markdown("Convertitore di Immagini in SVG - Creato con Streamlit e Potrace") 