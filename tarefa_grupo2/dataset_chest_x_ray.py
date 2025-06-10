import kagglehub
import pandas as pd
import os
import shutil # Importa o módulo shutil para manipulação de arquivos e pastas

# Define o caminho da pasta do seu script
# A variável __file__ dá o caminho completo do script atual
# os.path.dirname() pega apenas o diretório
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Diretório do script: {script_dir}")

# Define o nome da pasta de destino para o dataset dentro do seu script_dir
destination_folder_name = "coronahack_dataset"
destination_path = os.path.join(script_dir, destination_folder_name)

# Garante que a pasta de destino exista
os.makedirs(destination_path, exist_ok=True)

# Baixa a versão mais recente para o cache padrão
downloaded_path = kagglehub.dataset_download("praveengovi/coronahack-chest-xraydataset")
print(f"Conjunto de dados baixado (cache padrão): {downloaded_path}")

# Lista o conteúdo do diretório baixado para encontrar o caminho correto
# Já sabemos que o CSV está na raiz, e as imagens na subpasta "Coronahack-Chest-XRay-Dataset"
source_metadata_file = os.path.join(downloaded_path, "Chest_xray_Corona_Metadata.csv")
source_images_folder = os.path.join(downloaded_path, "Coronahack-Chest-XRay-Dataset")

# Move/Copia os arquivos para a pasta do script
try:
    # Copia o arquivo CSV de metadados
    shutil.copy(source_metadata_file, os.path.join(destination_path, "Chest_xray_Corona_Metadata.csv"))
    print(f"Metadados copiados para: {os.path.join(destination_path, 'Chest_xray_Corona_Metadata.csv')}")

    # Copia a pasta de imagens inteira (ou mova, se preferir não manter no cache)
    # Use copytree para copiar diretórios, precisa que o destino não exista
    if os.path.exists(os.path.join(destination_path, "Coronahack-Chest-XRay-Dataset")):
        shutil.rmtree(os.path.join(destination_path, "Coronahack-Chest-XRay-Dataset")) # Remove se já existir
    shutil.copytree(source_images_folder, os.path.join(destination_path, "Coronahack-Chest-XRay-Dataset"))
    print(f"Pasta de imagens copiada para: {os.path.join(destination_path, 'Coronahack-Chest-XRay-Dataset')}")

except Exception as e:
    print(f"Ocorreu um erro ao mover/copiar os arquivos: {e}")
    # Se os arquivos já existirem na pasta de destino, copytree pode falhar.
    # Considere usar shutil.rmtree(destination_path) antes de copiar, se você sempre quiser uma cópia fresca.

# Agora, o DataFrame é lido da nova localização
df_x_ray = pd.read_csv(os.path.join(destination_path, "Chest_xray_Corona_Metadata.csv"))

# Exibe as primeiras linhas do dataset
print("\nPrimeiras linhas do conjunto de dados (da nova localização):")
print(df_x_ray.head())
# Exibe o caminho para os arquivos do dataset (agora o caminho local)
print("\nCaminho local dos arquivos do conjunto de dados:", destination_path)