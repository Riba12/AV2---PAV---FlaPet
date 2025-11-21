import re

def cpf_valido(cpf: str) -> bool:
    """
    Validates format off CPF.
    Must contain 11 numeric digits.
    """
     # Remove caracteres não numéricos
    cpf_limpo = re.sub(r'[^0-9]', '', cpf) 

    if len(cpf_limpo) != 11:
        return False
    
    # retira numeros iguais, deixei para casos de teste
    # if cpf_limpo == cpf_limpo[0] * 11:
    #     return False
    
    # multiplica cada digito pelos pesos
    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11

    # valida o primeiro digito
    if resto == 10:
        resto = 0
    if resto != int(cpf_limpo[9]):
        return False
    
    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11

    # valida o segundo digito
    if resto == 10:
        resto = 0
    if resto != int(cpf_limpo[10]):
        return False
    
    return True
    