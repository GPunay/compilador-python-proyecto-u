import ply.lex as lex
import os

#lexer = lex
#Se definen las palabras reservadas (Esta se define como un objeto de python y no como una lista de cadenas de caracteres como en el caso del token)
reservadas = {
    'IF': 'if',
    'ELSE': 'else',
    'FOR' : 'for',
    'WHILE' : 'while',
    'DO' : 'do',
    'PRINT': 'print',
    'CONST': 'const'
}

listaReserv = list(reservadas)
valoresLista = list(reservadas.values())

tipo = {
    'INT':'int',
    'CHAR':'char',
    'FLOATING':'float',
    'STRING':'string',
    'BOOL':'bool'
}

listaTipo = list(tipo)
valorTipo = list(tipo.values())

# Definir los tokens
tokens = ['FLOAT', 'NUMBER',  'SUM', 'REST', 'MULT', 'DIV', 'POW', 'RESI', 'DOBLEEQUAL', 'EQUAL', 'DIF', 'PLUSS', 'MAYOR', 'MENOR', 'MAEQUAL', 'MEEQUAL', #OPERADORES
           'RPAREN', 'LPAREN', 'COMA', 'POINTCOMA', 'RLLAVE', 'LLLAVE', #delimitadores
           'AND', 'OR', #Operadores logicos
            'VAR',  #Variables Y constantes
            'CARACTER',
            'RESERV'] + listaReserv #Palabres reservadas
tokens.append('TIPO') #Lista de tipos de datos
for tip in listaTipo:    
    tokens.append(tip) #los tipos que acepta

# Definir las expresiones regulares para otros tokens
t_DOBLEEQUAL = r'\=\='
t_EQUAL = r'\=' 
t_DIF = r'\!\='
t_SUM = r'\+'
t_REST = r'-'
t_MULT = r'\*'
t_DIV =r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_POW = r'\^'
t_RESI = r'\%'
t_COMA = r'\,'
t_POINTCOMA = r'\;'
t_RLLAVE = r'\{'
t_LLLAVE = r'\}'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_PLUSS = r'\+\+'
t_MAYOR = r'\>'
t_MENOR = r'\<'
t_MAEQUAL = r'\>\='
t_MEEQUAL = r'\<\='
t_VAR = r'[a-zA-z_][a-zA-Z_0-9]*'#Permite que la expresion regular reconosca letras de la A-Z y numero
t_STRING = r'[\'|\"].*[\'|\"]' #Permite que al anteponer un '  o " y finalizar con ' o " lo detecte como una cadena de caracteres

def t_BOOL(t):
    r'FALSE|TRUE'
    t.type='BOOL'
    return t

def t_CHAR(t):
    r'\'.\''
    t.type='CHAR'
    return t

def t_TIPO(t):
    r'[a-zA-z_][a-zA-Z_0-9]*'
    flag = False
    for cadena in valorTipo:
        if t.value == cadena:
            t.type = reservadas.get(t.value, 'TIPO')
            flag=True
            break
    if not flag:
        t=t_RESERV(t)
    return t

def t_RESERV(t):
    r'[a-zA-z_][a-zA-Z_0-9]*'
    for cadena in valoresLista:
        if t.value == cadena:
            t.type = reservadas.get(t.value, 'RESERV')
            break
        else:
            t.type='VAR'
    return t
    

def t_FLOAT(t):
    r'\d+\.\d+'
    #print('float')
    try:
        t.value = float(t.value)  # Convertir el valor a flotante
    except ValueError:
        print("es un simbolo de texto")
        t.value = 0
    return t

# Definir la acción para el token NUMBER
def t_NUMBER(t):
    r'\d+'  # Esta es la expresión regular para un número
    #print('num')
    try:
        t.value = int(t.value)  # Convertir el valor a entero
    except ValueError:
        print("es un simbolo de texto")
        t.value = 0
    return t



#Es una funcion que define el salto del linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
 

# Definir reglas para ignorar espacios y saltos de línea
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"El caracter: {t.value[0]} no lo reconoce el lenguaje")
    t.lexer.skip(1)
    return 0

def analizadorLex(text):
    # Analizar una cadena
    #global lexer
    lexer = lex.lex()
    lexTemp = lex.lex()
    lexer.input(text)
    lexTemp.input(text) #Variable temporal para comprobar si todos los simbolos son reconocidos por la gramatica
    for flag in lexTemp:      
        if flag.type=='error':
            print('errorGram')
            return -1
    return lexer

def getTokens(lexer):
    # Imprimir los tokens
    nolinea = 1 #flag la cual servira para saber en que linea del codigo se encuentra el compilador
    lineacod = "" #Almacena una linea de tokens
    cadenaTokens="1.  " #Almacena todos los tokens correspondiente al codigo
    
    for token in lexer:        
        if(token.lineno !=nolinea):
            #print(token.value)
            cadenaTokens+=lineacod
            cadenaTokens+=f'\n\n{token.lineno}.  '
            lineacod=""
        lineacod += f"<{token.type}, {token.value}, {token.lexpos}>"
    
        nolinea=token.lineno 
    #print(lineacod)
    cadenaTokens+=lineacod
    return cadenaTokens

def crearTablaSimbolos(archivo, lexer):
    tree = []
    declaraciones = []
    with open(archivo, "w", encoding='utf-8') as tabla:
        tabla.write("ID".ljust(5)+"|Categoria".ljust(15)+"|Tipo".ljust(15) + "|Lexema".ljust(45) +"|valor".ljust(15) + "|linea".ljust(15) + "|Direccion de memoria\n".ljust(15))    
        tabla.write("-"*140 + "\n") 
        #print("ID".ljust(5)+"|Categoria".ljust(15)+"|Tipo".ljust(15) + "|Lexema".ljust(45) +"|valor".ljust(15) + "|linea".ljust(15) + "|Direccion de memoria\n".ljust(15))
        #print("-"*100 + "\n")
        for token in lexer:

            categoria=token.type
            tipo=""
            valor="-"
            lexema=token.value
            linea=token.lineno
            pos=token.lexpos

            if isinstance(token.value, int):
                tipo='INT'#token.type
                valor=token.value
                dir=hex(id(token))
            else:
                flag=0
                i=0
                valor="-"
                for reser in valoresLista:                                      
                    if reser==token.value:
                        flag=1
                        break
                    i+=1

                if flag==1:
                    tipo=listaReserv[i]
                else:
                    i=0
                    for tip in valorTipo:                                      
                        if tip==token.value:
                            flag=1
                            break
                        i+=1

                    if flag:
                        tipo=listaTipo[i]
                    else:
                        tipo=token.type

                dir=hex(id(token))
                #Se comprueba que en la tabla de simbolos no se repita la misma variable
                flag=0
                for vars in declaraciones:
                    if vars[1] == lexema:#Si la variable es la misma, comparte espacio de memoria y id
                        flag=1
                        dir=vars[2]
                        pos=vars[0]
                        break
                    
                if not flag:
                    simbol = [pos, lexema, dir]
                    declaraciones.append(simbol)

                #Se asigna el t

            #print(f"{pos}".ljust(5) + f" {categoria}".ljust(15) + f" {tipo}".ljust(15) +f" {lexema}".ljust(15) +f" {valor}".ljust(15) +f" {linea}".ljust(15) + " -\n")      
            fila =[f"{pos}", f" {categoria}", f" {tipo}",f" {lexema}", f" {valor}",f" {linea}", f" {hex(id(token))}\n"]
            tree.append(fila)
            tabla.write(f"{pos}".ljust(5) + f" {categoria}".ljust(15) + f" {tipo}".ljust(15) +f" {lexema}".ljust(45) +f" {valor}".ljust(15) +f" {linea}".ljust(15) + f" {hex(id(token))}\n")
        return tree
    
lexer = lex.lex()