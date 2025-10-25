from datetime import datetime

def validar_data(data_str):
    """
    Tenta validar uma string de data contra uma lista de formatos comuns.
    Retorna (True, 'Formato Detectado') se for válida,
    ou (False, 'Mensagem de Erro') se for inválida.
    """
    
    # Lista de formatos de data que queremos aceitar
    formatos_para_testar = [
        '%d/%m/%Y',  # Ex: 31/12/2024
        '%Y-%m-%d',  # Ex: 2024-12-31 (Formato ISO, o mais recomendado)
        '%d-%m-%Y',  # Ex: 31-12-2024
        '%m/%d/%Y',  # Ex: 12/31/2024 (Formato Americano)
        '%d/%m/%y',  # Ex: 31/12/24 (Ano com 2 dígitos)
    ]

    for formato in formatos_para_testar:
        try:
            # Tenta converter a string para data usando o formato
            datetime.strptime(data_str, formato)
            # Se a conversão for bem-sucedida, a data é válida e o formato existe
            return (True, f"Formato Válido: {formato}")
        except ValueError:
            # Se deu erro, tenta o próximo formato
            continue
    
    # Se o loop terminar sem sucesso, a data é inválida
    # Isso captura formatos desconhecidos (ex: '2024.12.31') 
    # OU datas logicamente inválidas (ex: '31/02/2024')
    return (False, "Erro: Formato inválido ou data logicamente incorreta (ex: 30/02)")

# --- SCRIPT DE TESTE ---
# Aqui estão as "variaveis diferencadas de datas" para validar:

datas_para_validar = [
    # Testes válidos (Formatos diferentes)
    "25/10/2025",   # Válido (Formato BR)
    "2025-10-25",   # Válido (Formato ISO)
    "25-10-2025",   # Válido (Híbrido)
    "10/25/2025",   # Válido (Formato US)
    "25/10/25",     # Válido (Ano curto)
    
    # Testes de Ano Bissexto
    "29/02/2024",   # Válido (2024 é ano bissexto)
    "29/02/2025",   # INVÁLIDO (2025 não é bissexto)
    
    # Testes logicamente inválidos
    "31/04/2024",   # INVÁLIDO (Abril só tem 30 dias)
    "30/02/2024",   # INVÁLIDO (Fevereiro não tem 30 dias)
    "13/31/2024",   # INVÁLIDO (Formato US com mês/dia trocado)
    "00/01/2024",   # INVÁLIDO (Dia 00)
    "01/00/2024",   # INVÁLIDO (Mês 00)
    
    # Testes de formato inválido
    "2024.10.25",   # INVÁLIDO (Formato não listado)
    "texto",        # INVÁLIDO (Não é data)
    "25-Out-2025"   # INVÁLIDO (Formato não listado)
]

print("--- Iniciando Teste de Validação de Datas ---")

resultados = {
    "Validos": [],
    "Invalidos": []
}

for data_teste in datas_para_validar:
    valido, mensagem = validar_data(data_teste)
    
    if valido:
        print(f"[ SUCESSO ] Data '{data_teste}': {mensagem}")
        resultados["Validos"].append(data_teste)
    else:
        print(f"[ FALHA   ] Data '{data_teste}': {mensagem}")
        resultados["Invalidos"].append(data_teste)

print("\n--- Resumo da Validação ---")
print(f"Total de Datas Válidas: {len(resultados['Validos'])}")
print(f"Total de Datas Inválidas: {len(resultados['Invalidos'])}")

from datetime import datetime

def validar_data_bissexto(data_str, formato='%d/%m/%Y'):
    """
    Tenta converter a string de data usando o formato especificado.
    Se a data for logicamente impossível (ex: 29/02/2023), retorna False.
    """
    try:
        # A função datetime.strptime é robusta e valida a lógica do calendário.
        # Por exemplo, ela lança ValueError para '30/02/2024' ou '29/02/2023'.
        datetime.strptime(data_str, formato)
        return (True, "Válida (Data e Formato Corretos)")
    except ValueError as e:
        # Captura o erro específico que indica uma data logicamente inválida.
        return (False, f"INVÁLIDA: {e}")

# --- LISTA DE DATAS PEGADINHAS (Casos Extremos e Impossíveis) ---

datas_pegadinhas = [
    # 1. Testes de ANO BISSEXTO (Onde a maioria falha)
    ("29/02/2024", True),   # 2024 é bissexto -> DEVE PASSAR (True)
    ("29/02/2023", False),  # 2023 NÃO é bissexto -> DEVE FALHAR (False)
    ("29/02/2000", True),   # 2000 é bissexto (Regra dos múltiplos de 400) -> DEVE PASSAR (True)
    ("29/02/1900", False),  # 1900 NÃO é bissexto (Regra dos múltiplos de 100, mas não de 400) -> DEVE FALHAR (False)
    
    # 2. Testes de Meses com 30 dias (31 dias em mês com 30)
    ("31/04/2025", False),  # Abril (mês 04) só tem 30 dias -> DEVE FALHAR (False)
    ("31/06/2025", False),  # Junho (mês 06) só tem 30 dias -> DEVE FALHAR (False)
    ("31/09/2025", False),  # Setembro (mês 09) só tem 30 dias -> DEVE FALHAR (False)
    ("31/11/2025", False),  # Novembro (mês 11) só tem 30 dias -> DEVE FALHAR (False)
    
    # 3. Testes de Datas Extremos/Limites
    ("01/01/2025", True),   # Dia de início (Limite Inferior) -> DEVE PASSAR (True)
    ("31/12/2025", True),   # Dia de fim (Limite Superior) -> DEVE PASSAR (True)
    ("32/01/2025", False),  # Dia impossível -> DEVE FALHAR (False)
    ("01/13/2025", False),  # Mês impossível -> DEVE FALHAR (False)
    ("00/01/2025", False),  # Dia zero (Impossível) -> DEVE FALHAR (False)
]

print("--- Iniciando Teste de Datas Pegadinhas (Formato: DD/MM/YYYY) ---")
print("------------------------------------------------------------------\n")

for data_teste, esperado_valido in datas_pegadinhas:
    valido, mensagem = validar_data_bissexto(data_teste)
    
    status = "[ SUCESSO ]" if valido == esperado_valido else "[ FALHA!!! ]"
    resultado = "Válida" if valido else "Inválida"
    
    print(f"{status} | Data: '{data_teste}' | Resultado: {resultado:<8} | Mensagem: {mensagem}")

print("\n------------------------------------------------------------------")
print("O campo '[ SUCESSO ]' indica que a função agiu como esperado.")
print("O campo '[ FALHA!!! ]' indica que a função não detectou a pegadinha.")

