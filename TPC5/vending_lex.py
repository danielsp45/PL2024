import ply.lex as lex
import ply.yacc as yacc
import sys

# Define tokens
tokens = (
    'LISTAR',
    'SELECIONAR',
    'SAIR',
    'SALDO',
    'MOEDA',
    'ITEM',
    'VALOR',
    'PONTO',
    'VIRGULA'
)

t_LISTAR = r'LISTAR'
t_SELECIONAR = r'SELECIONAR'
t_SAIR = r'SAIR'
t_SALDO = r'SALDO'
t_MOEDA = r'MOEDA'
t_ITEM = r'A-Z\d\d?'
t_VALOR = r'\d+[ce]'
t_PONTO = r'\.'
t_VIRGULA = r'\,'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)

t_ignore  = ' \t'


###############
# Program logic
###############

lexer = lex.lex()

DATA = {
    "items": [
        {
            "name": "Coca-Cola",
            "price": 1.0,
            "stock": 5,
            "code": "A1"
        },
        {
            "name": "Kinder Bueno White",
            "price": 1.0,
            "stock": 10,
            "code": "A2"
        }
    ],
    "balance": 0.0

}

def tokenize(s):
    lexer.input(s)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)

    return tokens

def program_loop():
    data = DATA.copy()

    while True:
        s = input('>>> ')
        tokens = tokenize(s)
        if len(tokens) == 0:
            print('Comando inválido')
            continue
        command = tokens[0].value
        handle_command(command, tokens, data)
        
def handle_command(command, tokens, data):
    if command == 'LISTAR':
        list_items(data)
    elif command == 'SELECIONAR':
        selecionar_item(tokens, data)
    elif command == 'SAIR':
        print('Sair')
        sys.exit(0)
    elif command == 'SALDO':
        print(f"Saldo: {data['balance']:.2f} €")
    elif command == 'MOEDA':
        insert_money(tokens, data)
    else:
        print('Comando inválido')

def list_items(data):
    items = data['items']

    if items.count == 1:
        print('Não há itens disponíveis')
        return
    for item in items:
        print(f"{item['code']}: {item['name']} - {item['price']:.2f} €")

def selecionar_item(tokens, data):
    if tokens[1].type != 'ITEM':
        print('Item inválido')
        return
    item = tokens[1].value
    item_data = get_item_by_code(item, data['items'])

    if not item_data:
        print('Item não encontrado')
        return

    if data['balance'] < item_data['price']:
        print('Saldo insuficiente')
        print(f"Saldo: {data['balance']:.2f} €")
        print(f"Preço: {item_data['price']:.2f} €")
        return
    else:
        print(f"Item selecionado: {item_data['name']}")
        data['balance'] -= item_data['price']
        item_data['stock'] -= 1
        print(f"Saldo restante: {data['balance']:.2f} €")


def get_item_by_code(code, items):
    for item in items:
        if item['code'] == code:
            return item
    return None

def insert_money(tokens, data):
    value = 0.0
    for token in tokens[1:]:
        if token.type == 'VALOR':
            if token.value[-1] == 'c':
                value += float(token.value.replace('c', '')) / 100
            elif token.value[-1] == 'e':
                value += float(token.value.replace('e', ''))
    data['balance'] += value
    print(f"Saldo: {data['balance']:.2f} €")


if __name__ == '__main__':
    program_loop()
