
import pandas as pd
import csv
import json

class FileTransform:

    @staticmethod
    def remover_quebras_linha(conteudo):
        """Remove quebras de linha (LF e CR) do conteúdo de uma string."""
        return conteudo.replace('\n', ' ').replace('\r', '')
    
    @staticmethod
    def remover_espacos_iniciais_finais(conteudo):
        """Remove espaços em branco no início e no fim da string."""
        return conteudo.strip()

    @staticmethod
    def substituir_delimitador(conteudo, delimitador_atual, novo_delimitador):
        """Substitui um delimitador no conteúdo de uma string."""
        return conteudo.replace(delimitador_atual, novo_delimitador)
    
    @staticmethod
    def remover_linhas_vazias(conteudo):
        """Remove linhas vazias do conteúdo de uma string (separado por linhas)."""
        return [linha for linha in conteudo.splitlines() if linha.strip() != '']

    @staticmethod
    def remover_duplicados_csv(file_path: str):
        """Remove linhas duplicadas de um arquivo CSV."""
        df = pd.read_csv(file_path)
        df.drop_duplicates(inplace=True)
        df.to_csv(file_path, index=False)

    @staticmethod
    def limpar_coluna_csv(file_path, coluna, valor_substituir=None):
        """Limpa valores nulos ou ausentes de uma coluna no CSV."""
        df = pd.read_csv(file_path)
        df[coluna] = df[coluna].fillna(valor_substituir)
        df.to_csv(file_path, index=False)

    @staticmethod
    def corrigir_tipo_dados_csv(file_path, coluna, tipo_dado):
        """Corrige o tipo de dado de uma coluna no CSV."""
        df = pd.read_csv(file_path)
        df[coluna] = df[coluna].astype(tipo_dado)
        df.to_csv(file_path, index=False)

    @staticmethod
    def verificar_json_formatado(json_data):
        """Verifica se uma string está no formato JSON válido."""
        try:
            json.loads(json_data)
            return True
        except ValueError as e:
            print("Erro de formatação JSON:", e)
            return False

    @staticmethod
    def json_para_csv(json_file, csv_file):
        """Converte um arquivo JSON para CSV."""
        with open(json_file, 'r') as f:
            data = json.load(f)
        df = pd.json_normalize(data)
        df.to_csv(csv_file, index=False)

    @staticmethod
    def remover_campo_json(json_file, campo):
        """Remove um campo específico de um arquivo JSON."""
        with open(json_file, 'r') as f:
            data = json.load(f)
        for item in data:
            if campo in item:
                del item[campo]
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def filtrar_json(json_file, chave, valor):
        """Filtra dados no arquivo JSON com base em uma chave e valor."""
        with open(json_file, 'r') as f:
            data = json.load(f)
        filtered_data = [item for item in data if item.get(chave) == valor]
        return filtered_data

    @staticmethod
    def txt_para_json(txt_file: str, json_file: str):
        """Converte um arquivo TXT para JSON, criando um dicionário para cada linha."""
        with open(txt_file, 'r') as f:
            lines = f.readlines()
        data = [{"linha": line.strip()} for line in lines]
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def preencher_valores_nulos_csv(file_path: str, valor_default=''):
        """Preenche valores nulos em um arquivo CSV com o valor default fornecido."""
        df = pd.read_csv(file_path)
        df.fillna(valor_default, inplace=True)
        df.to_csv(file_path, index=False)

    @staticmethod
    def ler_csv_personalizado(file_path: str, delimitador=';'):
        """Lê um arquivo CSV com um delimitador personalizado."""
        return pd.read_csv(file_path, delimiter=delimitador)

    @staticmethod
    def ler_arquivo_com_encoding(file_path: str, encoding='utf-8'):
        """Lê um arquivo com o encoding especificado."""
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
        
    @staticmethod
    def converter_encoding_arquivo(file_path: str, encoding_destino: str):
        """
        Converte o encoding de um arquivo para o encoding especificado.

        Args:
            file_path (str): Caminho do arquivo a ser convertido.
            encoding_destino (str): O encoding para o qual o arquivo será convertido (ex: 'utf-8', 'ascii', 'iso-8859-1').

        Returns:
            None: Modifica o arquivo original ou cria um novo arquivo com o encoding alterado.
        """
        try:
            # Lê o arquivo com o encoding atual (assumimos que o arquivo esteja em UTF-8)
            with open(file_path, 'r', encoding='utf-8') as file:
                conteudo = file.read()

            # Escreve o conteúdo no novo arquivo com o encoding desejado
            with open(file_path, 'w', encoding=encoding_destino) as file:
                file.write(conteudo)
            
            print(f"Arquivo {file_path} convertido para {encoding_destino} com sucesso.")
        
        except UnicodeDecodeError as e:
            print(f"Erro ao ler o arquivo: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

