import re
from datetime import datetime

class DataTransformations:

    @staticmethod
    def limpar_cpf(cpf: str) -> str:
        """Remove os caracteres especiais do CPF."""
        return re.sub(r'\D', '', cpf)

    @staticmethod
    def limpar_cnpj(cnpj: str) -> str:
        """Remove os caracteres especiais do CNPJ."""
        return re.sub(r'\D', '', cnpj)
    
    @staticmethod
    def formatar_cpf(cpf: str) -> str:
        """Formata o CPF para o formato padrão (XXX.XXX.XXX-XX)."""
        cpf = DataTransformations.limpar_cpf(cpf)
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @staticmethod
    def formatar_cnpj(cnpj: str) -> str:
        """Formata o CNPJ para o formato padrão (XX.XXX.XXX/XXXX-XX)."""
        cnpj = DataTransformations.limpar_cnpj(cnpj)
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Valida se o CPF é válido usando o algoritmo de validação de CPF."""
        cpf = DataTransformations.limpar_cpf(cpf)
        if len(cpf) != 11:
            return False
        # Algoritmo de validação do CPF
        def calcular_digito(cpf: str, pesos: list) -> int:
            soma = sum(int(digit) * weight for digit, weight in zip(cpf, pesos))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        cpf_base = cpf[:9]
        digitos = cpf[9:]
        peso1 = list(range(10, 1, -1))
        peso2 = list(range(11, 2, -1))

        digito1 = calcular_digito(cpf_base, peso1)
        digito2 = calcular_digito(cpf_base + str(digito1), peso2)
        return digitos == f"{digito1}{digito2}"

    @staticmethod
    def limpar_data(data: str) -> str:
        """Remove barras ou traços de datas e converte para o formato ddmmaaaa."""
        return re.sub(r'\D', '', data)

    @staticmethod
    def formatar_data(data: str, formato: str = "%d/%m/%Y") -> str:
        """Formata uma data de string para o formato especificado."""
        try:
            return datetime.strptime(data, "%Y-%m-%d").strftime(formato)
        except ValueError:
            return data

    @staticmethod
    def converter_para_datetime(data: str) -> datetime:
        """Converte uma string para um objeto datetime."""
        try:
            return datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            return None

    @staticmethod
    def substituir_caracteres_especiais(conteudo: str) -> str:
        import unicodedata
        import re

        """
        Substitui caracteres especiais no conteúdo de uma string, incluindo acentos, ç, ', e :.
        
        Args:
            conteudo (str): O conteúdo no qual os caracteres especiais serão substituídos.
        
        Returns:
            str: O conteúdo com os caracteres especiais substituídos por espaços ou letras correspondentes.
        """
        # Remove acentos e caracteres especiais com ~ e ç
        conteudo = unicodedata.normalize('NFKD', conteudo)
        conteudo = conteudo.encode('ASCII', 'ignore').decode('ASCII')
        
        # Substitui os caracteres especiais, incluindo ' e :
        caracteres_especiais = r"[;/´`\"'\\:]"  # Inclui ' e :
        conteudo_tratado = re.sub(caracteres_especiais, ' ', conteudo)
        
        return conteudo_tratado

    @staticmethod
    def formatar_valor(valor: str) -> float:
        """Converte um valor monetário (string) para float, removendo separadores de milhar e vírgulas."""
        valor = re.sub(r'[^\d,]', '', valor)
        valor = valor.replace(',', '.')
        return float(valor)

    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida se o formato do email é válido."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(email_regex, email))

    @staticmethod
    def formatar_numero(numero: float, casas_decimais: int = 2) -> str:
        """Formata um número com o separador de milhar e com a quantidade de casas decimais especificada."""
        return f"{numero:,.{casas_decimais}f}"

