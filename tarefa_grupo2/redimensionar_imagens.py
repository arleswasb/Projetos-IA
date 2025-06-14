from PIL import Image
import os
import logging
import sys

# Configura o logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def resize_images_for_cnn(input_folder: str, output_folder: str, size: tuple = (224, 224), 
                          quality: int = 90, output_format: str = 'jpeg'):
    """
    Redimensiona todas as imagens em uma pasta de entrada e suas subpastas
    para um tamanho padrão, salvando-as em uma pasta de saída.

    Args:
        input_folder (str): Caminho para a pasta que contém as imagens originais.
        output_folder (str): Caminho para a pasta onde as imagens redimensionadas serão salvas.
        size (tuple): Uma tupla (largura, altura) em pixels para o redimensionamento.
                      Ex: (224, 224) para a maioria das CNNs pré-treinadas.
        quality (int): Qualidade para imagens JPEG (0-100). Ignorado para PNG e outros formatos sem perda.
        output_format (str): Formato de saída para todas as imagens redimensionadas (ex: 'jpeg', 'png').
                             Isso garante consistência. Se o formato original for diferente, será convertido.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Pasta de saída '{output_folder}' criada.")

    processed_count = 0
    skipped_count = 0
    total_files = sum([len(files) for r, d, files in os.walk(input_folder)]) # Estima o total para progresso

    logging.info(f"Iniciando redimensionamento de imagens de '{input_folder}' para '{output_folder}' com tamanho {size} e formato de saída '{output_format}'...")

    # Percorre todos os arquivos e pastas no diretório de entrada
    for root, _, files in os.walk(input_folder):
        # Calcula o caminho relativo da subpasta para recriá-la na pasta de saída
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)

        # Cria a subpasta na pasta de saída se não existir (exist_ok=True evita erro se já existir)
        os.makedirs(output_subfolder, exist_ok=True)

        for file in files:
            input_image_path = os.path.join(root, file)
            # Define o nome do arquivo de saída com a nova extensão, se o formato de saída for diferente
            output_file_name = f"{os.path.splitext(file)[0]}.{output_format}"
            output_image_path = os.path.join(output_subfolder, output_file_name)

            try:
                with Image.open(input_image_path) as img:
                    # Tenta converter para RGB para evitar problemas com imagens em modo 'P' ou 'L'
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Redimensiona a imagem usando um filtro de alta qualidade
                    img_resized = img.resize(size, Image.LANCZOS)

                    # Salva a imagem redimensionada no formato de saída especificado
                    save_params = {}
                    if output_format.lower() in ['jpeg', 'jpg']:
                        save_params['quality'] = quality
                    elif output_format.lower() == 'png':
                        # PNGs são lossless, qualidade não se aplica, mas pode-se controlar compressão
                        # save_params['compress_level'] = 9 # Exemplo de parâmetro PNG
                        pass
                    
                    img_resized.save(output_image_path, format=output_format, **save_params)

                    processed_count += 1
                    # Exibe progresso a cada 100 imagens ou a cada 10% do total
                    if processed_count % 100 == 0 or (total_files > 0 and processed_count % (total_files // 10) == 0):
                        logging.info(f"Progresso: {processed_count}/{total_files} imagens processadas.")

            except FileNotFoundError:
                logging.warning(f"Arquivo não encontrado: '{input_image_path}'. Ignorando.")
                skipped_count += 1
            except Image.UnidentifiedImageError:
                logging.warning(f"Não foi possível identificar a imagem: '{input_image_path}'. Ignorando.")
                skipped_count += 1
            except Exception as e:
                logging.error(f"Erro inesperado ao processar a imagem '{input_image_path}': {e}")
                skipped_count += 1

    logging.info(f"\nRedimensionamento concluído!")
    logging.info(f"Imagens processadas: {processed_count}")
    logging.info(f"Arquivos ignorados/com erro: {skipped_count}")

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # Define as pastas de entrada e saída
    # Assume que o script está no mesmo diretório que a pasta 'dataset_classificado'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    original_dataset_root = os.path.join(script_dir, "dataset_classificado","imagens")
    resized_output_root = os.path.join(script_dir, "coronahack_dataset_resized")

    # Verifica se a pasta de dados original existe antes de prosseguir
    if not os.path.exists(original_dataset_root):
        logging.error(f"A pasta de entrada '{original_dataset_root}' não foi encontrada.")
        logging.error("Por favor, certifique-se de que o caminho está correto e a pasta existe.")
        sys.exit(1) # Sai do script com erro

    # Tamanhos comuns para CNNs (largura, altura)
    target_size = (128, 128)  # Exemplo: 128x128 pixels, pode ser ajustado conforme necessário
    
    # Chama a função para redimensionar as imagens
    resize_images_for_cnn(original_dataset_root, resized_output_root, target_size, output_format='jpeg')

    logging.info(f"\nAs imagens redimensionadas estão disponíveis em: {resized_output_root}")
    logging.info("Você pode verificar a pasta para confirmar os resultados.")