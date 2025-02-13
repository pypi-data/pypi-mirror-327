from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import csv

class GCPBigQuery:
    def __init__(self, project_id: str):
        """
        Construtor da classe GCPBigQuery
        :param project_id: ID do projeto no GCP. Se None, o projeto do ambiente será usado.
        """
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id

    def run_query(self, query: str):
        """
        Executa uma consulta SQL no BigQuery e retorna os resultados.
        :param query: Consulta SQL a ser executada.
        :param project_id: ID do projeto no GCP.
        :return: Resultados da consulta.
        """
        query_job = self.client.query(query, project=self.project_id)

        # Aguarda o job e obtém resultados
        results = query_job.result()
        return results
    
    def insert_data(self, dataset_id: str, table_id: str, rows: list):
        """
        Insere dados em uma tabela do BigQuery.
        :param dataset_id: ID do dataset onde a tabela está localizada.
        :param table_id: Nome da tabela onde os dados serão inseridos.
        :param rows: Lista de dicionários com os dados a serem inseridos.
        :return: Resultado da operação de inserção.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        try:
            # Insere os dados e verifica se houve erros
            errors = self.client.insert_rows_json(table_ref, rows)
            
            # Verifica se não houve erros na inserção
            if errors == []:
                return "Dados inseridos com sucesso."
            else:
                return f"Erros ao inserir dados: {errors}"
        except NotFound as e:
            return f"Tabela {table_id} não encontrada: {e}"
        except Exception as e:
            return f"Ocorreu um erro ao tentar inserir os dados: {e}"

    def update_data(self, query: str):
        """
        Atualiza dados em uma tabela do BigQuery usando uma consulta SQL.
        :param query: Consulta SQL de atualização.
        :return: Resultado da execução da consulta.
        """
        return self.run_query(query)

    def delete_data(self, query: str):
        """
        Deleta dados em uma tabela do BigQuery usando uma consulta SQL.
        :param query: Consulta SQL de deleção.
        :return: Resultado da execução da consulta.
        """
        return self.run_query(query)

    def create_table(self, dataset_id: str, table_id: str, schema: list):
        """
        Cria uma tabela no BigQuery.
        :param dataset_id: ID do dataset onde a tabela será criada.
        :param table_id: Nome da tabela que será criada.
        :param schema: Esquema da tabela (lista de dicionários com campos e tipos).
        :return: Mensagem de sucesso ou erro.
        """
        schema = [bigquery.SchemaField(field['name'], field['type']) for field in schema]
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        try:
            self.client.create_table(table)
            return f"Tabela {table_id} criada com sucesso."
        except Exception as e:
            return f"Erro ao criar a tabela: {e}"

    def delete_table(self, dataset_id: str, table_id: str):
        """
        Deleta uma tabela do BigQuery.
        :param dataset_id: ID do dataset onde a tabela está localizada.
        :param table_id: Nome da tabela a ser deletada.
        :return: Mensagem de sucesso ou erro.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        try:
            self.client.delete_table(table_ref)
            return f"Tabela {table_id} deletada com sucesso."
        except NotFound as e:
            return f"Tabela {table_id} não encontrada: {e}"
        except Exception as e:
            return f"Erro ao deletar a tabela: {e}"
    
    def load_data_from_gcs(self, dataset_id: str, table_id: str, gcs_uri: str, schema: list, source_format='CSV'):
        """
        Carrega dados de um arquivo no Google Cloud Storage para uma tabela no BigQuery.
        :param dataset_id: ID do dataset no BigQuery.
        :param table_id: ID da tabela no BigQuery.
        :param uri: URI do arquivo no GCS (exemplo: 'gs://bucket_name/file.csv').
        :param source_format: Formato do arquivo (default: 'CSV').
        :param project_id: ID do projeto no GCP.
        """
        # Definindo a referência da tabela no BigQuery
        table_ref = self.client.dataset(dataset_id).table(table_id)

        # Configuração do job de carga
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            source_format=source_format,
            autodetect=False,
        )

        # Inicia o Job de carga
        load_job = self.client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
        load_job.result()

        print(f"Dados carregados para a tabela {dataset_id}.{table_id} a partir de {gcs_uri}.")

    def execute_query_export(self, query: str, output_file: str, output_format='csv', header=True):
        """
        Executa uma consulta no BigQuery e exporta o resultado para um arquivo CSV ou TXT.
        :param query: A consulta SQL a ser executada.
        :param output_file: Nome do arquivo de saída (exemplo: 'resultados.csv' ou 'resultados.txt').
        :param output_format: Formato do arquivo de saída ('csv' ou 'txt').
        :param include_header: Se True, inclui o cabeçalho no arquivo de saída. Caso contrário, não inclui.
        :param project_id: ID do projeto no GCP.
        """
        # Executa a consulta no BigQuery
        query_job = self.client.query(query)
        results = query_job.result()

        # Verifica o formato da saida do arquivo
        if output_format == 'csv':
            # Abre o arquivo em modo escrita
            with open(output_file, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Escreve o cabeçalho se for True
                if header:
                    writer.writerow([field.name for field in results.schema])

                # Escreve as linhas com os dados
                for row in results:
                    writer.writerow(row.values())

            print(f"Dados exportados para {output_file} em formato CSV.")

        elif output_format == 'txt':
            # Abre o arquivo em modo escrita
            with open(output_file, mode='w') as txtfile:
                # Se 'header' for True, escreve o cabeçalho
                if header:
                    headers = "\t".join([field.name for field in results.schema])
                    txtfile.write(headers + "\n")

                # Escreve as linhas com os dados
                for row in results:
                    row_data = "t".join([str(value) for value in row.values()])
                    txtfile.write(row_data + "\n" )

            print(f"Dados exportados para {output_file} em formato TXT.")

        else:
            raise ValueError("Formato de saída não suportado. Use 'csv' ou 'txt'.")

