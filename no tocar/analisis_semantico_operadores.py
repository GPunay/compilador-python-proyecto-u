#Este documento contiene las reglas semanticas las cuales el lenguaje acepta.
# #La libreria que ayudara a crear la estructura gramatical que pueden tener la lineas de codigo del lenguaje
import ply.yacc as yacc
import ply.gramatica as gram
from ply.gramatica import tokens

#Variables globales
id=[]
categoria=[]
tipo=[]
linea=0
dir=''
#Variable que detecta un error en la compilacion del programa
redFlag=0
#Cadena de caracteres que almacenara los mensajes de error
errores=""
#Esta tabla de simbolos funcionara como una tabla catalogo para determinar los valores, tipos y declaraciones de las variables del programa
TablaSim = []
tokens_list = []

#Es la precendencia de los operadores, entre mas abajo esten mas precedencia tienen
precedence = (
    ('left', 'SUM', 'REST'),
    ('left', 'MULT', 'DIV'))



#Funcion para determinar cuantos token hay en una linea

def lengToken(line):
    lengLine=0
    lengLine=len(line)
    return lengLine

#Funcion para obtener los datos de un token
def get_data(lexema):
    global TablaSim
    temp = TablaSim
    flag=False
    tonken=[]

    for tokens in temp:
        if tokens[1]==lexema:
            token=tokens
            flag=True
    if flag:
        return token
    return None

#Funcion para devolver todos los datos del token en base a su posicion
def get_data_asig(lexema, line):
    global TablaSim
    temp = TablaSim
    token = []
    for tokens in temp:

        if tokens[1]==lexema and int(tokens[5])<=int(line):
            token= tokens
        if int(tokens[5])>int(line):

            print(lexema)
            print("fin:::")
            break
    print(tokens[5])
    print(line)        
    print("Token"+str(token))
    return token

#Funcion para obtener el tipo de un token en especifico de la tabla de simbolos
def get_tipo(lexema):
    global tokens_list
    temp=tokens_list
    for token in temp:
        
        if token[1]==str(lexema):
            return token[2]
    return None

def set_valor(lexema, pos, valor):
    global tokens_list
    temp=tokens_list
    i=-1
    for token in temp:
        i+=1
        if token[1]==str(lexema) and token[5]==pos:
            tokens_list[i][4]=valor
            return tokens_list
    return None
#start = 'condicional'

def p_bloque(p):
    '''bloque : declaracion
            | condicional
            | ciclo
            | imprimir
            | asignacion
            | bloque bloque'''
    #print("bloque de codigo")
    #prueba(p)
    p[0]=p[1]

def p_declaracion(p):
    '''declaracion : TIPO VAR EQUAL expresion POINTCOMA
                    | TIPO VAR EQUAL CHAR POINTCOMA
                    | TIPO VAR EQUAL STRING POINTCOMA
                    | TIPO VAR EQUAL BOOL POINTCOMA
                    | TIPO VAR EQUAL VAR POINTCOMA
                    | TIPO VAR POINTCOMA'''
    #Condicion para que no se pueda declara una variable existente
    global errores
    if(declarada(p[2])):#Si la variable ya esta declarada entonces no se puede declarar nuevamente
        token=get_data(p[2])
        errores+="La variable " + p[2] + " ya esta declarada como tipo: " + str(token[3]) + "\n"
        p_error(p)
    else:
        global TablaSim

        #Analizar si es una declaracion o una instancia de una variable
        if (p[3]!='='):
            cadena = [id[1], p[2], categoria[1], tipo[0], '-', linea]
            p[0]=p[2]
        
        else:#Si se instancia una variable se comprueba que el tipo sea el adecuado para la variable
                  
            if tipo[3]=='VAR':#Se hacen evaluaciones si se esta inicializando con una variable ya existenete
                if  declarada(p[4]):#Si la variable si existe
                    token = get_data(p[4])
                    tipo[4]=token[3]
                    if token[3]==tipo[0]:#Si las variables son del mismo tipo
                        cadena = [id[1], p[2], categoria[1], tipo[0], token[4], linea]
                        p[0]=p[2]
                    else:
                        errores+="Error: No se puede inicializar una variable tipo " + tipo[0] + " como una dato tipo " + tipo[4] + "\n"
                        p_error(p)
                else:
                    errores+="Error: La variable : " + p[4] + " no esta declarada.\n"
                    p_error(p)
             #char
            # #string
            #bool  
            elif tipo[0]==tipo[3]:#Se evalua si se asigna algun valor constante que el tipo corresponda al valor constante
                cadena = [id[1], p[2], categoria[1], tipo[0], p[4], linea]
                p[0]=p[2]
            else:#Si el tipo de dato no es el adecuado
                errores+="Error: No se puede inicializar una variable tipo " + tipo[0] + " como una dato tipo " + tipo[4] + "\n"
                p_error(p)
            #expresiones
        if p[0]!=None: #Solo si no hubo un error se agregara la variable a la tabla de simbolos
            TablaSim.append(cadena)
            #print("Declaracion Exitosa")
            #print(TablaSim)

    #print("declaracion")
    #print(p[2])
    #prueba(p)

#Funcion que determina que una variable ya este o no declarada
def declarada(id):
    global TablaSim
    flag=0
    for sim in TablaSim:
        if sim[1]==id:
            flag=1
            return flag
    return flag

#Regla para poder asignar un valor a una variable
def p_asignacion(p):
    '''asignacion : VAR EQUAL expresion POINTCOMA
                    | VAR EQUAL CHAR POINTCOMA
                    | VAR EQUAL STRING POINTCOMA
                    | VAR EQUAL BOOL POINTCOMA
                    | VAR EQUAL VAR POINTCOMA'''
    #Condicion para no se pueda asignar un valor a una variable indefinida
    global errores
    if not declarada(p[1]):
        errores+="Error en la asignacion: La variable " + p[1] + " no esta declarada\n"
        p_error(p)
    else:
        token1 = get_data(p[1])
        tipo[0]=token1[3]

        #Se evalua si es una asignacion de un valor o el resultado de una operacion
        token2=get_data(p[3])
        
        print(token1[3])
        print(p[3])

        if token2!=None:#Evaluaciones para determinar si se esta asignando el valor de una variable a otra
            if  declarada(p[3]):#Si la variable si existe                      
                tipo[2]=token2[3]
                print("Tokens: ")
                
                print(token2[3])
                if token1[3]==token2[3]:#Si las variables son del mismo tipo
                    cadena = [id[0], p[1], categoria[0], tipo[0], token2[4], linea]
                    p[0]=p[2]
                else:
                    errores+="Error de asignacion: No se puede inicializar una variable tipo " + tipo[0] + " como una dato tipo " + tipo[2]+"\n"
                    p_error(p)
            else:
                errores+="Error de Asignacion: La variable : " + str(p[3]) + " no esta declarada.\n"
                p_error(p)
            #char
            # #string
            #bool  
        elif tipo[0]==tipo[2]:#Se evalua si se asigna algun valor constante que el tipo corresponda al valor constante
            cadena = [id[0], p[1], categoria[0], tipo[0], p[3], linea]
            p[0]=p[2]
        elif (tipo[0]=='INT' or tipo[0]=='FLOATING') and isinstance(p[3], (int, float)):#Se comprueba si el valor es numerico, pare redondear valores de ser necesario
            
            if tipo[0]=='INT' and isinstance(p[3], (float)):#Se redondea el numero
                p[3]=int(p[3])

            cadena = [id[0], p[1], categoria[0], tipo[0], p[3], linea]
            p[0]=p[2]
        else:#Si el tipo de dato no es el adecuado
            errores+="Error de Asignacion: No se puede inicializar una variable tipo " + tipo[0] + " con el valor: " +str(p[3]) + "\n"
            p_error(p)
            #expresiones
    if p[0]!=None: #Si no hubo un error se agregara la variable a la tabla de simbolos
        TablaSim.append(cadena)

        set_valor(p[1],linea, p[3])


        print("Asignacion Exitosa")
        #print(TablaSim)

    #Condicion para asegurar que el tipo de la asignacion y la variable sean los mismos.
    #print("asignacion")
    #prueba(p)
    p[0]=p[3]


#las reglas semanticas para las operaciones aritmeticas basicas con numeros enteros y flotantes
#Las expresiones son las operaciones que detecta el analizador, la secuencia acepta una expresion seguida de un operado, seguida de otra expresion o un factor
def p_expresion(p):
    '''expresion : expresion SUM expresion
                 | expresion REST expresion
                 | expresion MULT expresion
                 | expresion DIV expresion'''
    #print("Expresion")
    #prueba(p)
    #Error: no se puede dividir un numero dentro de 0.
    global errores
    if p[2]=='/' and p[3]==0:
        errores+="No se puede dividir un numero dentro de 0.\n"
        p_error(p)
    else:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

#Convierte un nodo expresion a un nodo factor (terminal)
def p_exp_factor(p):
    'expresion : factor'
    p[0]=p[1]


#Reglas de los factores
def p_factor_int(p):#Se aceptan numeros enteros
    'factor : NUMBER'
    p[0]=p[1]

def p_facto_exp(p):#SE aceptan expresiones encerradas en parentesis
    'factor : LPAREN expresion RPAREN'
    p[0]=p[2]

def p_factor_float(p):#Se aceptan numero floatantes
    'factor : FLOAT'
    p[0]=p[1]

#El resultado de un factor tambien puede ser una variable
def p_factor_var(p):
    'factor : VAR'
    global errores
    #debe de haber una condicion que verifique la existencia de la variable
    if not declarada(p[1]):
        errores+="La variable " + p[1] + " no esta declarada\n"
        p_error(p)
    else:
        token=get_data(p[1])
        #print(token)
        p[0]=token[4]

#Reglas semanticas para las palabras reservadas
#reglas semanticas del if
def p_condicional(p):
    '''condicional : RESERV condiciones RLLAVE fin_con
                    | RESERV condiciones RLLAVE fin_con RESERV RLLAVE fin_con'''
    #print("if")
    #prueba(p)
    global errores
    #Posibles errores con la funcion if
    if p[1]!= 'if':
        errores+="Error: La construccion del if esta incorrecta.\n"
        p_error(p)
    else:
        if len(p)>5 and p[5]!='else':
            errores+="Error en la construccion del else\n"
            p_error(p)
        p[0] = p[1]

def p_fin_condi(p):
    '''fin_con : bloque LLLAVE'''
    p[0]=p[1]

#Para que se permitan mas de una condicion
def p_codiciones(p):
    '''condiciones : logica
                    | LPAREN logica AND logica RPAREN
                    | LPAREN logica OR logica RPAREN'''
    p[0]=p[1]

#Operaciones logicas
def p_operacion_logica(p):
    '''logica : LPAREN factor op_log factor RPAREN'''
    #Comprobar que el operador logico sea valido con el tipo de variable (CHAR==CHAR)
    global errores
    if p[3]=='==':
        #Se comprueba que la comparacion se con el mismo tipo de dato
        if get_tipo(p[2])!=get_tipo(p[4]):
            errores+="Error: La comparacion se debe de realizar con los mismo tipos de datos\n"
            p_error(p)
    elif (p[3]=='<' or p[3]=='>' or p[3] == '<=' or p[3]=='>='): #Se evalua que la comparaciones de mayor y menor solo se realicen con datos numericos
        tipo1=get_tipo(p[2])
        tipo2=get_tipo(p[4])
       
        if tipo1=='VAR':
            tipo1=get_data(p[2])[3]
        if tipo2=='VAR':
            tipo2=get_data(p[4])

        if(tipo1=='INT' or tipo1=='FLOAT') and (tipo1=='INT' or tipo2=='FLOAT'):
            print("Se ha realizado la comparacion adecuadamente")
        else:
            errores+="Error: La operacion logica se realizo de manera incorrecta, corrobore los tipos y las variables\n"
            p_error(p)
        
    else:
        errores+="Error: La operacion logica se realizo de manera incorrecta, corrobore los tipos y las variables\n"
        p_error(p)
    #print("operacion logica")
    #prueba(p)
    p[0]=p[2]

#Reglas semanticas del ciclo while
def p_while(p):
    '''ciclo : RESERV condiciones RLLAVE fin_con RESERV POINTCOMA'''
    #print("while")
    #prueba(p)
    #Posible errores en el while
    global errores
    if p[1]!= 'while':
        errores+="Error: La construccion del while esta mal hecha\n"
        p_error(p)
    elif p[5]!= 'do':
        errores+="Error: Falta la sentencia do; para cerrar ciclo while\n"
        p_error(p)
    else:
        p[0] = p[1]

#Operadores logicos
def p_op_logico(p):
    '''op_log : MAYOR 
            | MENOR 
            | MAEQUAL
            | MEEQUAL
            | DOBLEEQUAL
            | DIF'''
    #print("op logicos")
    #prueba(p)
    p[0]=p[1]

#Reglas semanticas para la funcion print
def p_print(p):
    '''imprimir : RESERV LPAREN STRING RPAREN POINTCOMA
                | RESERV LPAREN CHAR RPAREN POINTCOMA
                | RESERV LPAREN expresion RPAREN POINTCOMA'''
    #print("Print")
    #prueba(p)
    global errores
    #Posibles errores con la funcion print
    if p[1]!="print":
        errores+="Error: uso incorrecto de la funcion print\n"
        p_error(p)
    else:
        p[0]=p[3]

#El manejador de errores del analisis semantico
def p_error(p):
    global redFlag
    global errores
    try:
        p=None
        errores+="Error logico o de sintaxis en la linea: " + str(linea) + "\n"
    except EOFError:
        errores+="Error logico o de sintaxis en la linea: " + str(linea) + "\n"
    redFlag=1


# Construcción del parser
parser = yacc.yacc()

#funcion para realizar el analisis de una linea de codigo
def analisis_linea(bloque):
    global id
    global linea
    global categoria
    global tipo
    r=parser.parse(bloque)
    id=[]
    categoria=[]
    tipo=[]

#Funcion para leer la tabla de simbolos para extraer los datos importantes
#Esta funcion creara una tabla de simbolos sintetizada donde se almacenaran las variables generadas para asegurarse de la correcta utilizacion en las operaciones que ofrece el lenguaje
#Se encargara de obtener el mensaje de error y devolverlo a al modulo main.py para mostrarlo en la GUI.

def analizador_semantico(tokens):
    global id
    global linea
    global categoria
    global tipo
    global tokens_list
    global redFlag
    global errores
    global TablaSim
    global tokens_list

    #Se reinician las variables
    errores=""
    redFlag=0
    id=[]
    categoria=[]
    tipo=[]
    linea=0
    dir=''
    tokens_list=[]
    TablaSim=[]

    bloque=""
    lineaCod=1
    flag = False #Determina si el if esta compuesto por un else
    flagIf=False
    flagWhile=False
    i=0
    try:
        for ids, cat, tip, lexema, valor, pos, dir in tokens:
            if i==0:
                i=1
                lineaCod=pos
            #Si se detecta un error durante la compilacion
            if(redFlag):
                break

            if lineaCod!=pos and bloque!="" and (not flagIf and not flagWhile):
                analisis_linea(bloque)
                bloque=""
                lineaCod=pos

            #bloque+=lexema + " "

            if lexema=="if" or flagIf:
                flagIf=True
                if flag and lexema!='else':
                    
                    flag=False
                    flagIf=False
                    #print(bloque)
                    analisis_linea(bloque)
                    bloque=""
                    lineaCod=pos
                if lexema=='}':                 
                    flag=True

            if lexema=="while" or flagWhile:
                flagWhile=True
                if flag and lexema==';':
                    flag=False
                    flagWhile=False
                else:
                    print("Error: no se finalizo correctamente el ciclo while")
                if lexema=='do':
                    flag=True

            id.append(ids)
            categoria.append(cat)
            tipo.append(tip)
            linea=(pos)
            bloque+=lexema + " "
            tokens_list.append([ids, lexema, tip,cat, valor, pos, dir])

            
            #bloque.append(valor)
        analisis_linea(bloque)
        if not redFlag:
            
            nueva_tabla()
            return redFlag, ""
        else:
            errores+="Realice las correcciones correspondientes\n"
            return redFlag, errores
    except EOFError:
        errores+="Error durante el analisis del semantico del código\n"
        return redFlag, errores

#Funcion para sobreescribir en la tabla de simbolos y graficar la tabla catalogo de variables
def nueva_tabla():
    global TablaSim
    global tokens_list
    temp = []

    with open("tabla_simbolos.txt", "w", encoding='utf-8') as tabla1:
        tabla1.write("ID".ljust(5)+"|Categoria".ljust(15)+"|Tipo".ljust(15) + "|Lexema".ljust(45) +"|valor".ljust(15) + "|linea".ljust(15) + "|Direccion de memoria\n")    
        tabla1.write("-"*140 + "\n") 
        for token in tokens_list:
            print("Simbolos")
            print(token)
            if token[2]=='VAR':
                tok=get_data_asig(token[1], token[5])
                token[2]=tok[3]
                token[4]=tok[4]
            temp=token
            tabla1.write(f"{temp[0]}".ljust(5) + f" {temp[3]}".ljust(15) + f" {temp[2]}".ljust(15) +f" {temp[1]}".ljust(45) +f" {temp[4]}".ljust(15) +f" {temp[5]}".ljust(15) + f" {temp[6]}\n")
 
      
    with open("tabla_simbolos_variables.txt", "w", encoding='utf-8') as tabla:
        tabla.write("ID".ljust(5)+"|Lexema".ljust(15)+"|Categoria".ljust(15) + "|Tipo".ljust(45) +"|valor".ljust(15) + "|linea\n")
        tabla.write("-"*140 + "\n")
        for token in TablaSim:
            tabla.write(f"{token[0]}".ljust(5) + f" {token[1]}".ljust(15) + f" {token[2]}".ljust(15) +f" {token[3]}".ljust(45) +f" {token[4]}".ljust(15) +f" {token[5]}".ljust(15)+"\n")
    return 0
          
        