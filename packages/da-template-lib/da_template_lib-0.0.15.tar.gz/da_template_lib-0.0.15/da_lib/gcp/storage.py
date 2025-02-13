from google.cloud import storage
import csv

class GCPStorage:
    def __init__(self, project_id=None):
        """
        Construtor da classe GCPStorage
        :param project_id: ID do projeto no GCP. Se None, o projeto do ambiente será usado.
        """
        self.client = storage.Client(project=project_id)

    def upload_blob(self, bucket_name: str, source_file_name: str, destination_blob_name: str):
        """
        Faz o upload de um arquivo para um bucket no GCP Storage.
        :param bucket_name: Nome do bucket no GCP.
        :param source_file_name: Caminho local do arquivo a ser enviado.
        :param destination_blob_name: Nome do blob (arquivo) no bucket.
        """
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(f"Arquivo {source_file_name} enviado para {destination_blob_name} no bucket {bucket_name}.")

    def download_blob(self, bucket_name: str, source_blob_name: str, destination_file_name: str):
        """
        Faz o download de um arquivo de um bucket no GCP Storage.
        :param bucket_name: Nome do bucket no GCP.
        :param source_blob_name: Nome do blob (arquivo) no bucket.
        :param destination_file_name: Caminho local onde o arquivo será salvo.
        """
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f"Arquivo {source_blob_name} baixado para {destination_file_name}.")

    def delete_blob(self, bucket_name: str, blob_name: str):
        """
        Exclui um arquivo (blob) de um bucket no GCP.
        :param bucket_name: Nome do bucket no GCP.
        :param blob_name: Nome do arquivo (blob) no GCP.
        """
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        print(f"Arquivo {blob_name} excluído do bucket {bucket_name}.")

    def count_files_in_folder(self, bucket_name: str, folder_prefix: str):
        """
        Conta o número de arquivos (blobs) dentro de uma pasta específica em um bucket no GCP Storage.
        :param bucket_name: Nome do bucket no GCP.
        :param folder_prefix: Prefixo da "pasta" no GCP Storage (como 'pasta/subpasta/').
        :return: Número de arquivos na pasta.
        """
        # Obtém o bucket
        bucket = self.client.get_bucket(bucket_name)

        # Lista os blobs no bucket com o prefixo (equivalente a uma pasta)
        blobs = bucket.list_blobs(prefix=folder_prefix)

        # Conta o número de arquivos dentro do prefixo (pasta), ignorando as pastas (prefixos)
        file_count = 0
        for blob in blobs:
            # Verifica se o blob não é apenas o "diretório" (termina com '/')
            if not blob.name.endswith('/'):
                file_count += 1
                print(f"Arquivo encontrado: {blob.name}")

        print(f"A pasta '{folder_prefix}' no bucket {bucket_name} contém {file_count} arquivos.")
        return file_count

    def count_lines_in_file(self, bucket_name: str, blob_name: str):
        """
        Conta o número de linhas em um arquivo armazenado no GCP Storage (como TXT, CSV, etc.).
        :param bucket_name: Nome do bucket no GCP.
        :param blob_name: Nome do arquivo (blob) no GCP.
        :return: Número de linhas no arquivo.
        """
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        content = blob.download_as_text()  # Lê o conteúdo como texto
        return len(content.splitlines())

    def read_file_content(self, bucket_name: str, blob_name: str, file_type='txt'):
        """
        Lê o conteúdo de um arquivo armazenado no GCP Storage e retorna como uma lista de linhas.
        Suporta arquivos TXT e CSV.
        :param bucket_name: Nome do bucket no GCP.
        :param blob_name: Nome do arquivo (blob) no GCP.
        :param file_type: Tipo do arquivo (padrão é 'txt'). Pode ser 'txt' ou 'csv'.
        :return: Conteúdo do arquivo como uma lista de linhas.
        """
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        if file_type == 'txt':
            content = blob.download_as_text()  # Lê o conteúdo como texto
            return content.splitlines()  # Retorna uma lista de linhas

        elif file_type == 'csv':
            content = blob.download_as_text()  # Lê o conteúdo como texto
            # Lê o conteúdo CSV e retorna como uma lista de dicionários
            lines = content.splitlines()
            reader = csv.DictReader(lines)
            return list(reader)

        else:
            raise ValueError(f"Tipo de arquivo '{file_type}' não suportado. Use 'txt' ou 'csv'.")

    def list_files_in_bucket(self, bucket_name, prefix=None):
        """
        Lista os arquivos em um bucket, com suporte a filtros de prefixo e sufixo.
        :param bucket_name: Nome do bucket no GCP.
        :param prefix: Prefixo dos arquivos a serem listados (opcional).
        :param suffix: Sufixo dos arquivos a serem listados (opcional).
        :return: Lista de nomes de arquivos no bucket.
        """
        bucket = self.client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs if not blob.name.endswith('/')]

    

