from tabulate import tabulate

CSV_FILE_PATH = "./Conte.csv"

# Posição dos campos de interesse a partir do 0
ID = 0
IDADE = 5
MODALIDADE = 8
CLUBE = 9
RESULTADO = 11

def processa_csv(file_path):
    """Lê o dataset a partir do file path dado e processa os dados a cada iteração"""
    try:
        with open(file_path, "r") as f:
            next(f)
            return f.readlines()

    except FileNotFoundError:
        print(f"Ficheiro {file_path} não encontrado")
        exit(1)

def processa_atletas(linhas, lista_modalidades, escaloes_atletas, atletas_aptos):
    for linha in linhas:
        campos = linha.split(',')
        processa_atleta(campos, lista_modalidades, escaloes_atletas, atletas_aptos)

def processa_atleta(campos, lista_modalidades, escaloes_atletas, atletas_aptos):
    """Processa um atleta individualmente, recolhendo os dados relevantes e guardando-os"""

    atleta = parse_linha(campos)

    guarda_escalao_atleta(atleta, escaloes_atletas)
    guarda_atleta_por_modalidade(atleta, lista_modalidades)
    contabiliza_atleta_apto(atleta, atletas_aptos)

def parse_linha(linha):
    """Dá parse de uma só linha para um dicionário"""
    return {
            "id": linha[ID],
            "idade": linha[IDADE],
            "modalidade": linha[MODALIDADE],
            "clube": linha[CLUBE],
            "resultado": linha[RESULTADO] == "true"
        }

def contabiliza_atleta_apto(atleta, atletas_aptos):
    """Caso o atleta esteja apto, contabiliza-o para a percentagem de atletas aptos"""
    if atleta["resultado"]:
        atletas_aptos[0] += 1

def guarda_escalao_atleta(atleta, escaloes_atletas):
    """Contabiliza escalão do atleta no dicionário de escaloes_atletas"""
    idade = atleta["idade"]

    if int(idade[1]) >= 5:
        escalao = "sub" + idade[0] + "9"
    else:
        escalao = "sub" + idade[0] + "4"

    if escalao in escaloes_atletas:
        escaloes_atletas[escalao] += 1
    else:
        escaloes_atletas[escalao] = 1

def guarda_atleta_por_modalidade(atleta, lista_modalidades):
    """Guarda a modalidade do atleta na lista ordenada alfabeticamente caso ainda não exista"""
    modalidade = atleta["modalidade"]

    end_loop = False
    i = 0
    while i < len(lista_modalidades) and not end_loop:
        if lista_modalidades[i].lower() == modalidade.lower():
            end_loop = True
        elif lista_modalidades[i].lower() > modalidade.lower():
            lista_modalidades.insert(i, modalidade)
            end_loop = True
        i += 1

    if not end_loop:
        lista_modalidades.append(modalidade)

if __name__ == "__main__":
    lista_modalidades = []
    escaloes_atletas = {}
    atletas_aptos = [0] # guardado dentro de uma lista para permitir mutabilidade

    linhas = processa_csv(CSV_FILE_PATH)
    processa_atletas(linhas, lista_modalidades, escaloes_atletas, atletas_aptos)

    # Tabela de atletas
    print("Lista de modalidades ordenadas alfabeticamente:")
    for modalidade in lista_modalidades:
        print(modalidade)
    # Percentagem de atletas aptos
    print("Percentagem de atletas aptos:", round((atletas_aptos[0] / len(linhas)) * 100, 2), "%")
    # Distribuição de atletas
    print("Distribuição de atletas por escalão:")
    for escalao, quantidade in escaloes_atletas.items():
        print(f"{escalao.capitalize()}: {quantidade}")
