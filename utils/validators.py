import re

def validar_cpf(cpf):
    """Remove formatação e verifica se tem 11 dígitos."""
    cpf = re.sub(r'\D', '', cpf)
    return len(cpf) == 11

def validar_cnpj(cnpj):
    """Remove formatação e verifica se tem 14 dígitos."""
    cnpj = re.sub(r'\D', '', cnpj)
    return len(cnpj) == 14

def limpar_cpf(cpf):
    return re.sub(r'\D', '', cpf)

def limpar_cnpj(cnpj):
    return re.sub(r'\D', '', cnpj)

def formatar_cpf(cpf):
    if cpf and len(cpf) == 11:
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
    return cpf

def formatar_cnpj(cnpj):
    if cnpj and len(cnpj) == 14:
        return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
    return cnpj
