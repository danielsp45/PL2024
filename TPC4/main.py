import ply.lex as lex

tokens = (
        'COMMAND',
        'FROM',
        'WHERE',
        'BIGGER_OR_EQUAL',
        'FIELD',
        "NUMBER",
        "DELIMITER"
    )

t_COMMAND = r'SELECT'
t_FROM = r'FROM'
t_WHERE = r'WHERE'
t_BIGGER_OR_EQUAL = r'>='
t_FIELD = r'\w+'
t_DELIMITER = r','
t_NUMBER = r'\d+'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore  = ' \t'

# Build the lexer
lexer = lex.lex()

# Test it out
data = 'SELECT id, nome, salario FROM empregados WHERE salario >= 820'

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break
    print(tok)
