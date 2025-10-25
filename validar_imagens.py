import xml.etree.ElementTree as ET
import requests

# Defina o nome do arquivo XML a ser lido
NOME_ARQUIVO_XML = 'signos.xml'

def extrair_urls_do_xml(nome_arquivo):
    """
    Carrega o XML, itera sobre os signos e extrai o nome e a URL da imagem.
    Retorna uma lista de tuplas: [(Nome do Signo, URL da Imagem), ...]
    """
    urls_de_imagens = []
    
    try:
        tree = ET.parse(nome_arquivo)
        root = tree.getroot()
        
        # Itera sobre todos os elementos <signo>
        for signo in root.findall('signo'):
            nome = signo.find('signoNome').text
            url_imagem = signo.find('imagem').text
            
            if nome and url_imagem:
                urls_de_imagens.append((nome, url_imagem))
            
        return urls_de_imagens

    except FileNotFoundError:
        print(f"ERRO: Arquivo '{nome_arquivo}' não encontrado. Certifique-se de que ele está no mesmo diretório.")
        return []
    except Exception as e:
        print(f"ERRO ao parsear o XML: {e}")
        return []


def validar_url(url):
    """
    Verifica se a URL retorna um código de status HTTP 200 (OK).
    Usa um método HEAD para ser mais rápido (não baixa o corpo da imagem).
    """
    try:
        # Timeout de 10 segundos para não travar o script em URLs lentas
        response = requests.head(url, timeout=10)
        
        if response.status_code == 200:
            return (True, "OK (200)")
        else:
            return (False, f"Falha ({response.status_code})")
            
    except requests.exceptions.Timeout:
        return (False, "Falha (Timeout)")
    except requests.exceptions.RequestException as e:
        return (False, f"Falha (Erro de Conexão: {e.__class__.__name__})")


# --- Execução Principal do Teste ---

print(f"--- Iniciando Teste de Validação de Imagens a partir de {NOME_ARQUIVO_XML} ---")

imagens_a_testar = extrair_urls_do_xml(NOME_ARQUIVO_XML)

if not imagens_a_testar:
    print("Nenhuma URL de imagem encontrada ou erro na leitura do XML. Encerrando.")
else:
    for nome_signo, url in imagens_a_testar:
        valida, mensagem = validar_url(url)
        
        status = "[ SUCESSO ]" if valida else "[ FALHA!!! ]"
        
        print(f"{status} | Signo: {nome_signo:<12} | URL: {url} | Status: {mensagem}")

print("\n--- Teste Concluído ---")