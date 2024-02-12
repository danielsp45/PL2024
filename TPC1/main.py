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

def processa_atletas(linhas, lista_atletas, escaloes_atletas, atletas_aptos):
    for linha in linhas:
        campos = linha.split(',')
        processa_atleta(campos, lista_atletas, escaloes_atletas, atletas_aptos)

def processa_atleta(campos, lista_atletas, escaloes_atletas, atletas_aptos):
    """Processa um atleta individualmente, recolhendo os dados relevantes e guardando-os"""

    atleta = parse_linha(campos)

    guarda_escalao_atleta(atleta, escaloes_atletas)
    guarda_atleta_por_modalidade(atleta, lista_atletas)
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

def guarda_atleta_por_modalidade(atleta, lista_atletas):
    """Guarda o objeto atleta na lista ordenada alfabeticamente por modalidade"""
    modalidade = atleta["modalidade"]

    inserted = False
    i = 0
    while i < len(lista_atletas) and not inserted:
        if lista_atletas[i]["modalidade"].lower() > modalidade.lower():
            lista_atletas.insert(i, atleta)
            inserted = True
        i += 1

    if not inserted:
        lista_atletas.append(atleta)

if __name__ == "__main__":
    lista_atletas = []
    escaloes_atletas = {}
    atletas_aptos = [0] # guardado dentro de uma lista para permitir mutabilidade

    linhas = processa_csv(CSV_FILE_PATH)
    processa_atletas(linhas, lista_atletas, escaloes_atletas, atletas_aptos)

    print("Percentagem de atletas aptos: ", round((atletas_aptos[0] / len(linhas)) * 100, 2), "%")
    print("Distribuição de atletas por escalao: ", escaloes_atletas)
    print("Lista de atletas ordenados por modalidade")
    for atleta in lista_atletas:
        print(atleta)
