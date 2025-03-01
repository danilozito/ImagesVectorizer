import numpy as np
import cv2
import potrace
import matplotlib.pyplot as plt
from PIL import Image
import argparse
import os
from svgwrite import Drawing

def preprocess_image(image_path, threshold=100, blur_kernel=5):
    """
    Prepara l'immagine per la vettorizzazione applicando:
    - Conversione a scala di grigi
    - Sfocatura per ridurre il rumore
    - Sogliatura per creare un'immagine binaria
    """
    # Carica immagine
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Impossibile caricare l'immagine da {image_path}")
    
    # Converti in scala di grigi
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Applica sfocatura per ridurre il rumore
    blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
    
    # Applica sogliatura
    _, binary = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
    
    return binary

def bitmap_to_potrace(bitmap):
    """
    Converte un'immagine bitmap binaria in curve potrace
    """
    # La libreria potrace richiede un array 1-bit
    bitmap = np.where(bitmap > 127, 0, 1).astype(np.uint32)
    
    # Crea bitmap e traccia contorni
    bm = potrace.Bitmap(bitmap)
    
    # Traccia i contorni e restituisci il percorso
    return bm.trace()

def generate_svg(path, output_path, image_width, image_height):
    """
    Genera un file SVG dai contorni tracciati
    """
    # Crea un nuovo disegno SVG
    dwg = Drawing(output_path, size=(image_width, image_height))
    
    # Aggiungi uno sfondo bianco
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
    
    # Crea un percorso SVG combinato per tutti i contorni
    path_data = ""
    
    # Aggiungi ogni curva al percorso SVG
    for curve in path:
        # Aggiungi il punto iniziale
        start_point = curve.start_point
        path_data += f"M{start_point[0]},{start_point[1]} "
        
        # Aggiungi ogni segmento
        for segment in curve:
            end_point = segment.end_point
            if segment.is_corner:
                # Linea retta
                c = segment.c
                path_data += f"L{c[0]},{c[1]} L{end_point[0]},{end_point[1]} "
            else:
                # Curva di Bezier
                c1 = segment.c1
                c2 = segment.c2
                path_data += f"C{c1[0]},{c1[1]} {c2[0]},{c2[1]} {end_point[0]},{end_point[1]} "
        
        # Chiudi il percorso
        path_data += "Z "
    
    # Aggiungi il percorso al disegno SVG con fill-rule="evenodd"
    # Questo gestisce automaticamente i contorni interni ed esterni
    dwg.add(dwg.path(d=path_data, fill='black', fill_rule='evenodd'))
    
    # Salva il file SVG
    dwg.save()

def process_image(input_path, output_path=None, threshold=100, blur=5, show_preview=False):
    """
    Processo completo di conversione da immagine raster a SVG
    """
    # Se non è specificato un percorso di output, usa lo stesso nome file con estensione .svg
    if output_path is None:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = f"{file_name}.svg"
    
    # Ottieni dimensioni dell'immagine originale
    with Image.open(input_path) as img:
        image_width, image_height = img.size
    
    # Preelabora l'immagine
    binary = preprocess_image(input_path, threshold=threshold, blur_kernel=blur)
    
    # Mostra l'anteprima del risultato binario se richiesto
    if show_preview:
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.imread(input_path)[..., ::-1])  # Converti BGR a RGB
        plt.title("Immagine originale")
        plt.subplot(1, 2, 2)
        plt.imshow(binary, cmap='gray')
        plt.title("Immagine binaria")
        plt.tight_layout()
        plt.show()
    
    # Converti in bitmap potrace
    path = bitmap_to_potrace(binary)
    
    # Genera il file SVG
    generate_svg(path, output_path, image_width, image_height)
    
    print(f"File SVG generato in: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Converti immagini raster in formato vettoriale SVG')
    parser.add_argument('-i', '--input', help='Percorso dell\'immagine da convertire (opzionale)')
    parser.add_argument('-o', '--output', help='Percorso di output per il file SVG (opzionale)')
    parser.add_argument('-t', '--threshold', type=int, default=100, 
                        help='Valore soglia per la binarizzazione (0-255, default: 100)')
    parser.add_argument('-b', '--blur', type=int, default=5,
                        help='Dimensione kernel per sfocatura (default: 5)')
    parser.add_argument('-p', '--preview', action='store_true',
                        help='Mostra anteprima dell\'immagine binarizzata')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Converti tutte le immagini da Images/ToConvert a Images/Converted')
    
    args = parser.parse_args()
    
    # Verifica se è richiesta la conversione di tutte le immagini
    if args.all or (args.input is None and args.output is None):
        # Crea le cartelle se non esistono
        input_dir = os.path.join("Images", "ToConvert")
        output_dir = os.path.join("Images", "Converted")
        
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
            print(f"Creata cartella {input_dir}")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Creata cartella {output_dir}")
        
        # Ottieni la lista di tutti i file nella cartella di input
        image_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and 
                      f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp'))]
        
        if not image_files:
            print(f"Nessuna immagine trovata in {input_dir}")
            return
        
        print(f"Trovate {len(image_files)} immagini da convertire...")
        
        # Converti ogni immagine
        for img_file in image_files:
            input_path = os.path.join(input_dir, img_file)
            file_name = os.path.splitext(img_file)[0]
            output_path = os.path.join(output_dir, f"{file_name}.svg")
            
            print(f"Conversione di {img_file}...")
            try:
                process_image(input_path, output_path, args.threshold, args.blur, args.preview)
                print(f"Convertito: {img_file} -> {file_name}.svg")
            except Exception as e:
                print(f"Errore durante la conversione di {img_file}: {str(e)}")
        
        print(f"Conversione completata. I file SVG sono stati salvati in {output_dir}")
    
    # Altrimenti processa solo il file specificato
    elif args.input:
        process_image(args.input, args.output, args.threshold, args.blur, args.preview)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()