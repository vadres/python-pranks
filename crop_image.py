import argparse
from PIL import Image
import os

def crop_image(image_path, width, height, image_padding=0, square_padding=0):
    # Abre a imagem
    image = Image.open(image_path)

    # Calcula o número de colunas e linhas necessárias para cobrir a imagem
    num_columns = (image.width + image_padding) // (width + square_padding)
    num_rows = (image.height + image_padding) // (height + square_padding)

    # Calcula o tamanho final da imagem
    final_width = num_columns * width + (num_columns - 1) * square_padding + 2 * image_padding
    final_height = num_rows * height + (num_rows - 1) * square_padding + 2 * image_padding

    # Adiciona padding à imagem
    padded_image = Image.new(image.mode, (final_width, final_height), (255, 255, 255, 0))
    padded_image.paste(image, (0, 0))

    # Cria uma pasta para salvar as imagens menores
    output_folder = "temp"
    os.makedirs(output_folder, exist_ok=True)

    # Corta a imagem em quadrados
    for row in range(num_rows):
        for col in range(num_columns):
            left = col * (width + square_padding) + image_padding
            upper = row * (height + square_padding) + image_padding
            right = left + width
            lower = upper + height
            cropped_image = padded_image.crop((left, upper, right, lower))
      
            # Salva a imagem cortada
            output_filename = os.path.join(output_folder, f"{row}_{col}.jpg")
            cropped_image.save(output_filename)

    print(f"{len(os.listdir(output_folder))} imagens salvas em {output_folder}")

if __name__ == "__main__":
    # Cria um parser de argumentos para receber os parâmetros
    parser = argparse.ArgumentParser(description='Corta uma imagem em quadrados menores')
    parser.add_argument('image', type=str, help='URL da imagem a ser cortada')
    parser.add_argument('width', type=int, help='Largura de cada quadrado em pixels')
    parser.add_argument('height', type=int, help='Altura de cada quadrado em pixels')
    parser.add_argument('--imagePadding', type=int, default=0, help='Tamanho do padding da imagem em pixels')
    parser.add_argument('--squarePadding', type=int, default=0, help='Tamanho do padding dos retangulos em pixels')
    args = parser.parse_args()

    # Chama a função crop_image com os parâmetros fornecidos pelo terminal
    crop_image(args.image, args.width, args.height, image_padding=args.imagePadding, square_padding=args.squarePadding)