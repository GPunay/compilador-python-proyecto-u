import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import ply.gramatica as grammar
import ply.analisis_semantico_operadores as an
import ply.lex as lex
#Modulo para ensamblar y compilar el programa
import ensamblador as compi
import os
import re
import graphviz
import pygame
import generar_arbolSem as gas
import generador_codigo_intermedio as gci
from generador_codigo_intermedio import generar_codigo_intermedio, optimizar_codigo_intermedio, generar_grafico_tac
from PIL import Image, ImageTk
from tkinter import filedialog

#Variables globales
texto_ingresado=""
strTokens=""
gram=grammar #Contiene las funciones de la gramatica del lenguaje
lexer=lex #Permite almacenar un objeto de tipo lexico, el cual contiene los tokens y la tabla de simbolos del programa
analizador_semantico = an #Modulo que contiene las funciones del analizador semantico
archiCodBase = "codigo_origen.txt"
archiTokens = "tokens.txt"
archiTabla = "tabla_simbolos.txt"
flagAnalizadorSem = False #Sera una badera que indicara si se puede realizar el codigo intermedio, solo si el analizador Semantico ha aceptado el codigo

#Función para abrir la ventana principal
def principal(parent):
    # Cerrar la ventana anterior antes de abrir una nueva ventana
    parent.destroy()
    # Creamos la ventana principal con un tamaño fijo, título e icono
    root = Tk()
    root.title("Compilador")
    root.geometry("1200x800")
    centrar_ventana(root, 1200, 800)
    
    # Colocamos la imagen de fondo de la ventana y la posicionamos
    imagenFondo = PhotoImage(file="Img/fondo_principal.png")
    fondo = Label(root, image=imagenFondo)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Mantener referencia de la imagen para evitar el recolector de basura
    fondo.image = imagenFondo
    
    # Creando mensaje de Bienvenida y posicionandolo
    bienvenida = Label(root, text="Bienvenido al Compilador!", bg="silver", fg="black", font=("Arial", 25, "bold"), bd=3, relief="ridge")
    bienvenida.place(x=200, y=25, width=500, height=60)
    
    # Creando un botón para Ingresar Texto al Editor
    botonEditor = Button(root, text="Ingresar Texto Editor", command=lambda: textoEditor(root), bg="deepskyblue", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonEditor.place(x=250, y=100, width=400, height=50)
    
    #Creando un botón para Analizador Léxico
    botonLexico = Button(root, text="Analizador Léxico", command=lambda: analisisLexico(root), bg="deepskyblue", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonLexico.place(x=250, y=175, width=400, height=50)
    
    #Creando un botón para Analizar Sintáctico
    botonSintactico = Button(root, text="Analizar Sintáctico", command=lambda: analisisSintactico(root), bg="deepskyblue", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonSintactico.place(x=250, y=250, width=400, height=50)
    
    #Creando un botón para tabla de Símbolos
    botonTabla = Button(root, text="Tabla de Símbolos", command=lambda: tablaSimbolos(root), bg="deepskyblue", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonTabla.place(x=250, y=325, width=400, height=50)
    
    #Creando un botón para Analizador Semántico
    botonSemantico = Button(root, text="Analizador Semántico", command=lambda: analizadorSemantico(root), bg="darkseagreen3", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonSemantico.place(x=250, y=400, width=400, height=50)
    
    #Creando un botón para Código intermedio
    botonIntermedio = Button(root, text="Código Intermedio", command=lambda: codigoIntermedio(root), bg="darkseagreen3", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonIntermedio.place(x=250, y=475, width=400, height=50)
    
    #Creando un botón para Optimizador
    botonOptimizador = Button(root, text="Optimizador de Codigo", command=lambda: optimizarCodigo(root), bg="darkseagreen3", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonOptimizador.place(x=250, y=550, width=400, height=50)
    
    #Creando un botón para Generador de Código
    botonGenerador = Button(root, text="Generador de Código", command=lambda: generarCodigo(root), bg="darkseagreen3", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonGenerador.place(x=250, y=625, width=400, height=50)
    
    #Creando un botón para Ejecutar
    botonEjecutar = Button(root, text="Ejecutar Código", command=lambda: ejecutarCodigo(root), bg="darkseagreen3", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonEjecutar.place(x=250, y=700, width=400, height=50)
    
    # Creando un botón para Salir del Programa
    botonSalir = Button(root, text="Salir", command=lambda: salirPrograma(root), bg="darkseagreen3", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonSalir.place(x=950, y=700, width=150, height=50)
    
    # Creando un botón para Limpiar Proyecto
    botonLimpiar = Button(root, text="Limpiar Proyecto", command=lambda: limpiar_proyecto(), bg="indianred", fg="white", font=("Arial", 16, "bold"), bd=4, relief="raised")
    botonLimpiar.place(x=750, y=700, width=180, height=50)
    
    # Mantenemos la ventana abierta
    root.mainloop()

# Función para Salir del Programa
def salirPrograma(parent):
    parent.destroy()
    
    #Creamos la ventana de despedida del programa
    despedida = Tk()
    despedida.title("Despedida")
    centrar_ventana(despedida, 1300, 800)
    despedida.iconbitmap("Img/compilador.ico")
    
    # Colocamos la imagen de fondo de la ventana y la posicionamos
    imagenDespedida = PhotoImage(file="Img/fondo_despedida.png")
    fondoDespedida = Label(despedida, image=imagenDespedida)
    fondoDespedida.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Mantener referencia de la imagen para evitar el recolector de basura
    fondoDespedida.image = imagenDespedida
    
    #Creamos un mensaje de despedida
    mensajeDespedida = Label(despedida, text="Gracias por usar el Compilador!", bg="ghost white", fg="black", font=("Arial", 25, "bold"), bd=3, relief="raised")
    mensajeDespedida.place(x=700, y=675, width=550, height=60)
    
    #Cerramos la ventana automáticamente después de 5 segundos
    despedida.after(5000, despedida.destroy)
    
#Funcion para guardar el texto ingresado
def guardarTexto(text_widget):
    
    if (text_widget.get("1.0", "end-1c") != ""):
        global texto_ingresado
        global lexer
        global strTokens
        global flagAnalizadorSem

        texto_temp = text_widget.get("1.0", END).strip()  # Obtener el texto del widget
        analizador = gram.analizadorLex(texto_temp) #almacena temporalmente el resultado del analizador lexico para asegurar que no hay errores
        if analizador==-1:#si se utiliza una simbologia que no reconoce el lenguaje no crea el analizador lexico
            print('Error en ingreso')
            texto_temp=""
            messagebox.showwarning('Advertencia', 'Hay un simbolo el cual no reconoce el lenguaje.')
        else:#si la simbologia corresponde a la gramatica entonces crea al analizador lexico
            lexer = analizador 
            texto_ingresado=texto_temp
            strTokens=gram.getTokens(analizador)
            escribirArchivo(archiTokens, strTokens)
            escribirArchivo(archiCodBase, texto_ingresado)
            print("Texto guardado:", texto_ingresado)  #Prueba de que el texto se ha guardado
            flagAnalizadorSem=False           
            messagebox.showinfo("Éxito en Guardar", "El texto se ha guardado correctamente")
        
    else:
   
        messagebox.showwarning("Advertencia", "No se ha ingresado ningun texto")

#Función para comprobar si ha ingresado texto en el editor de texto
def noAEscrito():
     messagebox.showerror("Error", "No ha ingresado ningun codigo, porfavor ingrese codigo para acceder a esta funcion.")

#Funcion para borrar el texto ingresado en el editor de texto
def borrar(text_widget):
    text_widget.delete("1.0", END)

def escribirArchivo(archivo, text):#funcion para escribir en los archivos de tokens, codigo_fuente y la tabla de simbolos
    with open(archivo, "w", encoding="utf-8") as txt:
        txt.write(text)
    print(f"\nArchivo {archivo} ha sido modificado\n")

#Fucnión para leer los archivos creados
def leerArchivo(archivo):
    with open(archivo, "r", encoding="utf-8") as txt:
        print(f"\nArchivo {archivo} ha sido leido correctamente\n")
        return txt.read()
        
    
#Vetanan para el editor de texto
def textoEditor(parent):
    # Cerrar la ventana anterior antes de abrir una nueva ventana
    parent.destroy()
    
    # Creamos la ventana principal con un tamaño fijo, título e icono    
    editor = Tk()
    editor.title("Ingreso de Texto al Editor")
    centrar_ventana(editor, 1200, 800)
    editor.iconbitmap("Img/compilador.ico")
    
    # Colocamos la imagen de fondo de la ventana y la posicionamos
    imagenEditor = PhotoImage(file="Img/fondo_editor.png")
    fondoEditor = Label(editor, image=imagenEditor)
    fondoEditor.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Mantener referencia de la imagen para evitar el recolector de basura
    fondoEditor.image = imagenEditor
    
    bienvenida = Label(editor, text="Editor de Texto", bg="azure2", fg="black", font=("Arial", 25, "bold"), bd=3, relief="ridge")
    bienvenida.place(x=425, y=100, width=400, height=60)
    
    # Boton para regresar al menu principal
    botonRegresar = Button(editor, text="Volver", command=lambda: principal(editor), bg="azure2", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonRegresar.place(x=900, y=640, width=150, height=50)
    
    #Boton para limpiar el cuadro de texto
    btnLimpiar = Button(editor, text='Borrar todo', command=lambda: borrar(text_widget,), bg="azure2", fg="black", font=("Arial", 16, "bold"), bd=4, relief="raised")
    btnLimpiar.place(x=725, y=640, width=150, height=50)

    text_widget = Text(editor, wrap=WORD, font=("Arial", 14))
    text_widget.place(x=150, y=200, width=900, height=400)
        
    botonGuardar = Button(editor, text="Guardar Texto", command=lambda: guardarTexto(text_widget), bg="azure2", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonGuardar.place(x=150, y=640, width=350, height=50)
    
    # Botón para nuevo proyecto
    btnNuevo = Button(editor, text='Nuevo Proyecto', command=lambda: nuevo_proyecto(editor, text_widget), bg="indianred", fg="white", font=("Arial", 16, "bold"), bd=4, relief="raised")
    btnNuevo.place(x=520, y=640, width=180, height=50)

    #Comprobar si ya hay codigo guardado para escribirlo    
    text_widget.insert("1.0", texto_ingresado)
    
    editor.mainloop()
    
#Ventana para realizar el análisis léxico
def analisisLexico(parent):
    
    
    if texto_ingresado != "":
        # Cerrar la ventana anterior antes de abrir una nueva ventana
        parent.destroy()
        # Creamos la ventana principal con un tamaño fijo, título e icono    
        lexico = Tk()
        lexico.title("Análisis Léxico")
        centrar_ventana(lexico, 1200, 800)
        lexico.iconbitmap("Img/compilador.ico")
        
        # Colocamos la imagen de fondo de la ventana y la posicionamos
        imagenLexico = PhotoImage(file="Img/fondo_lexico.png")
        
        fondoLexico = Label(lexico, image=imagenLexico)
        fondoLexico.place(x=0, y=0, relwidth=1, relheight=1)  
        # Mantener referencia de la imagen para evitar el recolector de basura
       
        #Textbox donde se mostraran los tokens generados
        fondoLexico.image = imagenLexico
        tokens = Text(lexico, width=90, height=20, font=("Arial", 14, "bold"), wrap="word")
        tokens.place(x=100, y=200)

        # Creando mensaje de Bienvenida y posicionandolo
        bienvenida = Label(lexico, text="Análisis Léxico", bg="dodgerblue1", fg="black", font=("Arial", 25, "bold"), bd=3, relief="ridge")
        bienvenida.place(x=425, y=100, width=400, height=60)
        
        # Creando un botón para Regresar al Menú principal
        botonRegresar = Button(lexico, text="Volver", command=lambda: principal(lexico), bg="bisque1", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
        botonRegresar.place(x=950, y=700, width=150, height=50)

        #Scrollbar para ver codigos grandes
        scrollbar = Scrollbar(lexico, command=tokens.yview)
        scrollbar.pack(side="right", fill='y')

        #Vincular la scrollbar
        tokens.config(yscrollcommand=scrollbar.set) 

        #Implementacion de las librerias PLY
        #strTokens=gram.getTokens(lexer)
        tokens.insert('1.0',strTokens)
        #escribirArchivo(archiTokens, strTokens)
         #print(gram.getTokens(lexer))
        tokens.config(state=DISABLED)

        # Mantenemos la ventana abierta
        lexico.mainloop()
    else:
        print(texto_ingresado)
        noAEscrito()

# Clase para representar el AST
class ASTNode:
    def __init__(self, tipo, valor=None, izquierdo=None, derecho=None):
        self.tipo = tipo
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

    def __repr__(self, nivel=0):
        indent = "  " * nivel
        resultado = f"{indent}{self.tipo}: {self.valor}\n"
        if self.izquierdo:
            resultado += self.izquierdo.__repr__(nivel + 1)
        if self.derecho:
            resultado += self.derecho.__repr__(nivel + 1)
        return resultado

# Función para leer los tokens del archivo
def leer_tokens(archivo="tokens.txt"):
    if not os.path.exists(archivo):
        return []
    
    with open(archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
    
    patron = r"<(\w+),\s*([^,]+),\s*(\d+)>"
    tokens = re.findall(patron, contenido)
    return [(tipo, valor, int(pos)) for tipo, valor, pos in tokens]

# Función para obtener la precedencia de un operador
def precedencia(operador):
    precedencias = {
        '=': 0, 
        'OR': 1,  
        'AND': 2, 
        'MAEQUAL': 3, 'MAYOR': 3, 'MENOR': 3, 'MEEQUAL': 3, 
        'SUM': 4, 'REST': 4, 
        'MULT': 5, 'DIV': 5, 'MOD': 5
    }
    return precedencias.get(operador, -1)

# Función para construir el árbol de sintaxis abstracta
def construir_ast(tokens):
    """
    Construye un árbol de sintaxis abstracta (AST) a partir de los tokens.
    Implementa un analizador recursivo descendente.
    """
    index = [0]  # Utilizamos una lista para permitir la modificación por referencia
    
    # Parsea el programa completo
    def parse_program():
        """Parsea el programa completo - secuencia de declaraciones."""
        statements = []
        while index[0] < len(tokens):
            stmt = parse_statement()
            if stmt:
                statements.append(stmt)
        
        # Si hay más de una declaración, creamos un nodo de programa
        if len(statements) > 1:
            return ASTNode("PROGRAM", None, statements, None)
        elif len(statements) == 1:
            return statements[0]
        else:
            return None
    
    # Parsea una sentencia individual
    def parse_statement():
        """Parsea una sentencia individual."""
        if index[0] >= len(tokens):
            return None
            
        token_type, token_value, _ = tokens[index[0]]
        
        # Declaración de variable: int x = 50;
        if token_type == "TIPO" and token_value in ["int", "float", "char", "bool", "string"]:
            return parse_declaration()
        
        # Sentencia if: if (condición) { ... }
        elif token_type == "RESERV" and token_value == "if":
            return parse_if_statement()
        
        # Sentencia while: while (condición) { ... }
        elif token_type == "RESERV" and token_value == "while":
            return parse_while_statement()
        
        # Sentencia print: print("Hola mundo");
        elif token_type == "RESERV" and token_value == "print":
            return parse_print_statement()
        
        # Asignación: x = 10;
        elif token_type == "VAR" and index[0] + 1 < len(tokens) and tokens[index[0] + 1][0] == "EQUAL":
            return parse_assignment()
        
        # Expresión individual (normalmente no debería ocurrir)
        else:
            expr = parse_expression()
            # Consumir punto y coma si existe
            if index[0] < len(tokens) and tokens[index[0]][0] == "POINTCOMA":
                index[0] += 1
            return expr
    
    # Función para parsear una declaración de variable
    def parse_declaration():
        """Parsea una declaración de variable: tipo nombreVar = valor;"""
        tipo_token = tokens[index[0]]
        index[0] += 1  # Consumir el tipo
        
        if index[0] >= len(tokens) or tokens[index[0]][0] != "VAR":
            return None  # Error: esperaba un nombre de variable
        
        var_token = tokens[index[0]]
        index[0] += 1  # Consumir el nombre de la variable
        
        # Nodo de declaración
        declaration_node = ASTNode("DECLARATION", tipo_token[1], None, None)
        var_node = ASTNode("VAR", var_token[1], None, None)
        declaration_node.izquierdo = var_node
        
        # Si hay una asignación (=)
        if index[0] < len(tokens) and tokens[index[0]][0] == "EQUAL":
            index[0] += 1  # Consumir el =
            expression = parse_expression()
            declaration_node.derecho = expression
        
        # Consumir punto y coma
        if index[0] < len(tokens) and tokens[index[0]][0] == "POINTCOMA":
            index[0] += 1
            
        return declaration_node
    
    # Función para parsear una sentencia if
    def parse_if_statement():
        """Parsea una sentencia if: if (condición) { ... }"""
        index[0] += 1  # Consumir el 'if'
        
        if_node = ASTNode("IF", None, None, None)
        
        # Consumir '('
        if index[0] < len(tokens) and tokens[index[0]][0] == "LPAREN":
            index[0] += 1
        else:
            return None  # Error: esperaba '('
        
        # Parsear la condición
        condition = parse_expression()
        if_node.izquierdo = condition
        
        # Consumir ')'
        if index[0] < len(tokens) and tokens[index[0]][0] == "RPAREN":
            index[0] += 1
        else:
            return None  # Error: esperaba ')'
        
        # Consumir '{'
        if index[0] < len(tokens) and tokens[index[0]][0] == "RLLAVE":
            index[0] += 1
        else:
            return None  # Error: esperaba '{'
        
        # Parsear el bloque de código
        block_statements = []
        while index[0] < len(tokens) and tokens[index[0]][0] != "LLLAVE":
            stmt = parse_statement()
            if stmt:
                block_statements.append(stmt)
        
        # Crear nodo de bloque
        if len(block_statements) > 0:
            block_node = ASTNode("BLOCK", None, block_statements, None)
            if_node.derecho = block_node
        
        # Consumir '}'
        if index[0] < len(tokens) and tokens[index[0]][0] == "LLLAVE":
            index[0] += 1
        
        return if_node
    
    # Función para parsear una sentencia while
    def parse_while_statement():
        """Parsea una sentencia while: while (condición) { ... }"""
        index[0] += 1  # Consumir el 'while'
        
        while_node = ASTNode("WHILE", None, None, None)
        
        # Consumir '('
        if index[0] < len(tokens) and tokens[index[0]][0] == "LPAREN":
            index[0] += 1
        else:
            return None  # Error: esperaba '('
        
        # Parsear la condición
        condition = parse_expression()
        while_node.izquierdo = condition
        
        # Consumir ')'
        if index[0] < len(tokens) and tokens[index[0]][0] == "RPAREN":
            index[0] += 1
        else:
            return None  # Error: esperaba ')'
        
        # Consumir '{'
        if index[0] < len(tokens) and tokens[index[0]][0] == "RLLAVE":
            index[0] += 1
        else:
            return None  # Error: esperaba '{'
        
        # Parsear el bloque de código
        block_statements = []
        while index[0] < len(tokens) and tokens[index[0]][0] != "LLLAVE":
            stmt = parse_statement()
            if stmt:
                block_statements.append(stmt)
        
        # Crear nodo de bloque
        if len(block_statements) > 0:
            block_node = ASTNode("BLOCK", None, block_statements, None)
            while_node.derecho = block_node
        
        # Consumir '}'
        if index[0] < len(tokens) and tokens[index[0]][0] == "LLLAVE":
            index[0] += 1
        
        return while_node
    
    #Función para parsear una impresión
    def parse_print_statement():
        """Parsea una sentencia print: print(expresión);"""
        index[0] += 1  # Consumir 'print'
        
        print_node = ASTNode("PRINT", None, None, None)
        
        # Consumir '('
        if index[0] < len(tokens) and tokens[index[0]][0] == "LPAREN":
            index[0] += 1
        else:
            return None  # Error: esperaba '('
        
        # Parsear la expresión
        expression = parse_expression()
        print_node.izquierdo = expression
        
        # Consumir ')'
        if index[0] < len(tokens) and tokens[index[0]][0] == "RPAREN":
            index[0] += 1
        else:
            return None  # Error: esperaba ')'
        
        # Consumir ';'
        if index[0] < len(tokens) and tokens[index[0]][0] == "POINTCOMA":
            index[0] += 1
        
        return print_node
    
    #Función para parsear una asignación
    def parse_assignment():
        """Parsea una asignación: variable = expresión;"""
        var_token = tokens[index[0]]
        index[0] += 1  # Consumir el nombre de la variable
        
        if index[0] >= len(tokens) or tokens[index[0]][0] != "EQUAL":
            return None  # Error: esperaba '='
        
        index[0] += 1  # Consumir el '='
        
        var_node = ASTNode("VAR", var_token[1], None, None)
        expression = parse_expression()
        
        # Crear nodo de asignación
        assignment_node = ASTNode("ASSIGNMENT", "=", var_node, expression)
        
        # Consumir punto y coma
        if index[0] < len(tokens) and tokens[index[0]][0] == "POINTCOMA":
            index[0] += 1
            
        return assignment_node
    
    #Función para parsear una expresión
    def parse_expression():
        """Parsea una expresión."""
        return parse_comparison()
    
    #Función para parsear una comparación
    def parse_comparison():
        """Parsea una comparación: expr1 >= expr2"""
        left = parse_additive()
        
        while index[0] < len(tokens) and tokens[index[0]][0] in ["MAYOR", "MENOR", "MAEQUAL", "MEEQUAL", "EQUAL", "NOEQUAL"]:
            op_token = tokens[index[0]]
            index[0] += 1  # Consumir el operador
            
            right = parse_additive()
            
            # Crear nodo de comparación
            left = ASTNode("COMPARISON", op_token[1], left, right)
        
        return left
    
    #Función para parsear una expresión aditiva
    def parse_additive():
        """Parsea una expresión aditiva: expr1 + expr2 o expr1 - expr2"""
        left = parse_multiplicative()
        
        while index[0] < len(tokens) and tokens[index[0]][0] in ["SUM", "REST"]:
            op_token = tokens[index[0]]
            index[0] += 1  # Consumir el operador
            
            right = parse_multiplicative()
            
            # Crear nodo aditivo
            left = ASTNode("ADDITIVE", op_token[1], left, right)
        
        return left
    
    #Función para parsear una expresión multiplicativa
    def parse_multiplicative():
        """Parsea una expresión multiplicativa: expr1 * expr2 o expr1 / expr2"""
        left = parse_primary()
        
        while index[0] < len(tokens) and tokens[index[0]][0] in ["MULT", "DIV", "MOD"]:
            op_token = tokens[index[0]]
            index[0] += 1  # Consumir el operador
            
            right = parse_primary()
            
            # Crear nodo multiplicativo
            left = ASTNode("MULTIPLICATIVE", op_token[1], left, right)
        
        return left
    
    #Función para parsear una expresión primaria
    def parse_primary():
        """Parsea una expresión primaria: literal, variable o expresión entre paréntesis."""
        if index[0] >= len(tokens):
            return None
            
        token_type, token_value, _ = tokens[index[0]]
        
        if token_type == "NUMBER":
            # Literal numérico
            index[0] += 1  # Consumir el número
            return ASTNode("NUMBER", token_value, None, None)
            
        elif token_type == "STRING":
            # Literal de cadena
            index[0] += 1  # Consumir la cadena
            return ASTNode("STRING", token_value, None, None)
        
        elif token_type == "CHAR":
            #Caracter
            index[0]+=1#consumir la cadena
            return  ASTNode("CHAR", token_value, None, None)

        elif token_type == "BOOL":
            #Literal booleana
            index[0]+=1
            return ASTNode("BOOL", token_value, None, None)
        elif token_type == "VAR":
            # Variable
            index[0] += 1  # Consumir la variable
            return ASTNode("VAR", token_value, None, None)
            
        elif token_type == "LPAREN":
            # Expresión entre paréntesis
            index[0] += 1  # Consumir '('
            expr = parse_expression()
            
            # Consumir ')'
            if index[0] < len(tokens) and tokens[index[0]][0] == "RPAREN":
                index[0] += 1
            else:
                return None  # Error: esperaba ')'
                
            return expr
            
        else:
            # Tipo desconocido
            index[0] += 1  # Consumir el token desconocido
            return None
    
    # Iniciar el parseo
    return parse_program()

#Función para generar el gráfico del árbol sintáctico
def generar_grafico_ast(arbol, filename):
    """
    Genera un gráfico del árbol de sintaxis abstracta usando Graphviz.
    
    Args:
        arbol: El nodo raíz del árbol AST.
        filename: Nombre del archivo de salida (sin extensión).
        
    Returns:
        Ruta del archivo de imagen generado.
    """
    dot = graphviz.Digraph(comment='Abstract Syntax Tree')
    dot.attr(rankdir='TB')  # Árbol de arriba hacia abajo
    dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
    
    # Función recursiva para recorrer el árbol y generar el gráfico
    def add_node(node, parent_id=None, edge_label=None):
        if not node:
            return
        
        # Crear un ID único para el nodo
        node_id = str(id(node))
        
        # Preparar la etiqueta del nodo
        if node.valor:
            label = f"{node.tipo}\\n{node.valor}"
        else:
            label = node.tipo
        
        # Añadir el nodo al grafo
        dot.node(node_id, label)
        
        # Añadir la conexión con el padre si existe
        if parent_id:
            if edge_label:
                dot.edge(parent_id, node_id, label=edge_label)
            else:
                dot.edge(parent_id, node_id)
        
        # Procesar los hijos
        if node.izquierdo:
            if isinstance(node.izquierdo, list):
                # Si es una lista de nodos (como en un bloque de código)
                for i, child in enumerate(node.izquierdo):
                    add_node(child, node_id, f"stmt{i+1}")
            else:
                # Si es un único nodo
                add_node(node.izquierdo, node_id, "left")
        
        if node.derecho:
            if isinstance(node.derecho, list):
                # Si es una lista de nodos (como en un bloque de código)
                for i, child in enumerate(node.derecho):
                    add_node(child, node_id, f"stmt{i+1}")
            else:
                # Si es un único nodo
                add_node(node.derecho, node_id, "right")


    # Añadir todos los nodos al grafo
    add_node(arbol)
    
    # Renderizar el grafo a un archivo de imagen
    try:
        # Intentar generar la imagen
        dot.render(filename, format='png', cleanup=True)
        return f"{filename}.png"
    except Exception as e:
        print(f"Error al generar el gráfico: {str(e)}")
        # Guardar el código DOT para depuración
        with open(f"{filename}.dot", "w") as f:
            f.write(dot.source)
        return None



#Error en caso de no existir la tabla de símbolos
def error_falta_tabla():
    messagebox.showerror("Error", "No se encontró la tabla de símbolos. Primero ejecute el análisis léxico y la generación de la tabla de símbolos.")

#Ventana de Análisis sintáctico
def analisisSintactico(parent):
    if not os.path.exists("tokens.txt"):
        error_falta_tabla()
        return
    
    parent.destroy()
    sintactico = tk.Tk()
    sintactico.title("Análisis Sintáctico")
    centrar_ventana(sintactico, 1200, 800)
    sintactico.iconbitmap("Img/compilador.ico")
    
    imagenSintactico = tk.PhotoImage(file="Img/fondo_sintactico.png")
    fondoSintactico = tk.Label(sintactico, image=imagenSintactico)
    fondoSintactico.place(x=0, y=0, relwidth=1, relheight=1)
    fondoSintactico.image = imagenSintactico
    
    bienvenida = tk.Label(sintactico, text="Análisis Sintáctico", bg="gainsboro", fg="black", font=("Arial", 25, "bold"), bd=3, relief="ridge")
    bienvenida.place(x=425, y=100, width=400, height=60)
    
    botonRegresar = tk.Button(sintactico, text="Volver", command=lambda: principal(sintactico), bg="ghostwhite", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonRegresar.place(x=950, y=725, width=150, height=50)
    
    # Crear un frame para mostrar mensajes
    mensaje_frame = tk.Frame(sintactico, bg="white", bd=4, relief="ridge")
    mensaje_frame.place(x=150, y=200, width=900, height=500)
    
    # Etiqueta para mostrar mensajes
    lbl_mensaje = tk.Label(mensaje_frame, text="Procesando tokens...", bg="white", font=("Arial", 14))
    lbl_mensaje.pack(pady=10)
    
    # Leer tokens y construir el AST
    try:
        tokens = leer_tokens()
        if not tokens:
            lbl_mensaje.config(text="Error: No se encontraron tokens para analizar.")
            return
        
        lbl_mensaje.config(text="Construyendo árbol de sintaxis abstracta...")
        sintactico.update()
        
        arbol = construir_ast(tokens)
        
        if not arbol:
            lbl_mensaje.config(text="Error: No se pudo construir el árbol sintáctico.")
            return
        
        lbl_mensaje.config(text="Generando visualización del árbol...")
        sintactico.update()
        
        # Generar la imagen del AST
        imagen_ast = generar_grafico_ast(arbol, "ast")
        
        if not imagen_ast or not os.path.exists(imagen_ast):
            lbl_mensaje.config(text="Error: No se pudo generar la imagen del árbol sintáctico.")
            return
        
        # Mostrar la imagen del AST
        lbl_mensaje.pack_forget()  # Ocultar el mensaje
        
        try:
            # Cargar y mostrar la imagen generada
            img = Image.open(imagen_ast)
            
            # Ajustar el tamaño de la imagen manteniendo la proporción
            width, height = img.size
            max_width = 850
            max_height = 650
            
            if width > max_width or height > max_height:
                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            img_tk = ImageTk.PhotoImage(img)
            
            # Crear un canvas para mostrar la imagen con scrollbars
            canvas = tk.Canvas(mensaje_frame, bg="white")
            scrollbar_y = tk.Scrollbar(mensaje_frame, orient="vertical", command=canvas.yview)
            scrollbar_x = tk.Scrollbar(mensaje_frame, orient="horizontal", command=canvas.xview)
            
            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")
            canvas.pack(side="left", fill="both", expand=True)
            
            # Añadir la imagen al canvas
            canvas.create_image(0, 0, anchor="nw", image=img_tk)
            canvas.image = img_tk  # Mantener una referencia
            
            # Configurar el área de scroll
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            # Crear un botón para guardar la imagen
            btn_guardar = tk.Button(
                sintactico, 
                text="Guardar", 
                command=lambda: guardar_imagen(imagen_ast),
                bg="cornsilk3", 
                fg="black", 
                font=("Arial", 20, "bold"), 
                bd=4, 
                relief="raised"
            )
            btn_guardar.place(x=525, y=725, width=200, height=50)
            
        except Exception as e:
            lbl_mensaje.config(text=f"Error al cargar la imagen: {str(e)}")
            lbl_mensaje.pack(pady=10)
    
    except Exception as e:
        lbl_mensaje.config(text=f"Error en el análisis sintáctico: {str(e)}")
    
    sintactico.mainloop()

#Función para guardar la imagen generada del Análisis Sintáctico
def guardar_imagen(imagen_origen):
    """Guarda una copia de la imagen generada en la ubicación que elija el usuario."""
    import shutil
    from tkinter import filedialog
    
    # Abrir diálogo para seleccionar dónde guardar
    ruta_destino = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Guardar árbol sintáctico"
    )
    
    if ruta_destino:
        try:
            # Copiar la imagen al destino seleccionado
            shutil.copy2(imagen_origen, ruta_destino)
            messagebox.showinfo("Éxito", "Imagen guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen: {str(e)}")

#Función para leer la tabla de símbolos
def leerTablaSimbolos(tabla_sim, tree, encabezado):
    # Definir encabezados y tamaño de columnas
    for col in encabezado:
        print(col)
        tree.heading(col, text=col)
        tree.column(col, width=143, anchor="center")

    for datos in tabla_sim:
        print(datos)
        tree.insert("", END, values=datos)


#Ventana de la Tabla de Símbolos
def tablaSimbolos(parent):
    if texto_ingresado!="":
        # Cerrar la ventana anterior antes de abrir una nueva ventana
        parent.destroy()
        
        # Creamos la ventana principal con un tamaño fijo, título e icono    
        tabla = Tk()
        tabla.title("Tabla de Simbolos")
        centrar_ventana(tabla, 1200, 800)
        tabla.iconbitmap("Img/compilador.ico")
        
        # Colocamos la imagen de fondo de la ventana y la posicionamos
        imagenTabla = PhotoImage(file="Img/fondo_tabla.png")
        fondoTabla = Label(tabla, image=imagenTabla)
        fondoTabla.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Mantener referencia de la imagen para evitar el recolector de basura
        fondoTabla.image = imagenTabla
        
        # Creando mensaje de Bienvenida y posicionandolo
        bienvenida = Label(tabla, text="Tabla de Simbolos", bg="darkseagreen4", fg="black", font=("Arial", 25, "bold"), bd=3, relief="ridge")
        bienvenida.place(x=425, y=100, width=400, height=60)
        
        # Creando un botón para Regresar al Menú principal
        botonRegresar = Button(tabla, text="Volver", command=lambda: principal(tabla), bg="tan4", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
        botonRegresar.place(x=950, y=700, width=150, height=50)
        
        #Se crea el archivo de la tabla de simbolos
        lexer = gram.analizadorLex(texto_ingresado)
        tabla_sim = gram.crearTablaSimbolos(archiTabla, lexer)

        #Frame para posicionar la tabla
        moverTabla = Frame(tabla, width=1000 ,height=400)
        # Evita que el marco cambie de tamaño por los elementos que contiene
        moverTabla.pack_propagate(False)
        moverTabla.pack(padx=1, pady=240)

        #Tabla utilizando treeview
        encabezado=["ID","Categoria","Tipo","Lexema","valor", "linea", "Direccion de memoria\n"] 
        tree = ttk.Treeview(moverTabla, columns=encabezado, show="headings", height=400)
        tree.pack()
        #Abrir el archivo de la tabla
        os.startfile(archiTabla)
        leerTablaSimbolos(tabla_sim, tree, encabezado)
        tree.pack()

        #Scrollbar para ver codigos grandes
        scrollbar = Scrollbar(moverTabla, command=tree.yview, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        tree.config(yscrollcommand=scrollbar.set)
        # Mantenemos la ventana abierta
        tabla.mainloop()
    else:
        noAEscrito()

#Ventana del Analizador Semántico
def analizadorSemantico (parent):
    if texto_ingresado!="":
        # Cerrar la ventana anterior antes de abrir una nueva ventana
        parent.destroy()
        
        # Creamos la ventana principal con un tamaño fijo, título e icono    
        semantico = Tk()
        semantico.title("Análisis Semántico")
        centrar_ventana(semantico, 1200, 800)
        semantico.iconbitmap("Img/compilador.ico")
        
        # Colocamos la imagen de fondo de la ventana y la posicionamos
        imagenSemantico = PhotoImage(file="Img/fondo_semantico.png")
        fondoSemantico = Label(semantico, image=imagenSemantico)
        fondoSemantico.place(x=0, y=0, relwidth=1, relheight=1)
        
        #Mantener la referencia a la imagen para evitar el recogedor de basura
        fondoSemantico.image = imagenSemantico
        
        #Creando mensajes de bienvenida y posicionándolos
        bienvenida = tk.Label(semantico, text="Análisis Semántico", bg="tomato3", fg="black", font=("Arial", 25, "bold"), bd=3, relief="ridge")
        bienvenida.place(x=425, y=100, width=400, height=60)
        
        botonRegresar = tk.Button(semantico, text="Volver", command=lambda: principal(semantico), bg="black", fg="white", font=("Arial", 20, "bold"), bd=4, relief="raised")
        botonRegresar.place(x=950, y=700, width=150, height=50)

        botonNuevaTabla = tk.Button(semantico, text="Ver Nueva tabla de simbolos", command=lambda: NewtablaSimbolos(semantico), bg="black", fg="white", font=("Arial", 20, "bold"), bd=4, relief="raised")
        botonNuevaTabla.place(x=500, y=700, width=400, height=50)
        
        global analizador_semantico
        #Se refresca la tabla de simbolos
        lexer = gram.analizadorLex(texto_ingresado)
        tabla_sim = gram.crearTablaSimbolos(archiTabla, lexer)
        #Se lee el archivo que tiene la definicion de los tokens paara obtener su data completa
        with open("tabla_simbolos.txt", "r", encoding="utf-8") as f:
            contenido = f.read()

        #Patro para leer en el archivo
        #(\d+)\s+(\w+)\s+(\w+)\s+(\w+|[^\s]+)\s+(-|\d+|[^\s]+)\s+(\d+)\s+(0x[0-9a-fA-F]+)
        patron = r"(\d+)\s+(\w+)\s+(\w+)\s+(\w+|[^\s]+|\".+\")\s+(-|\d+|[^\s]+)\s+(\d+)\s+(0x[0-9a-fA-F]+)" #r"<(\w+),\s*([^,]+),\s*(\d+)>"
        tokens = re.findall(patron, contenido)

        #Funcion para generar el analizador semantico y ver los errores
        flag, error = analizador_semantico.analizador_semantico(tokens)
        # Crear un frame para mostrar mensajes
        mensaje_frame = tk.Frame(semantico, bg="white", bd=4, relief="ridge")
        mensaje_frame.place(x=150, y=200, width=900, height=450)
        
        # Etiqueta para mostrar mensajes
        lbl_mensaje = tk.Label(mensaje_frame, text="Procesando tokens...", bg="white", font=("Arial", 14))
        lbl_mensaje.pack(pady=10)
        
        # Leer tokens y construir el AST
        if flag:
            messagebox.showerror("ERRORES GARRAFALES", error)
            lbl_mensaje.config(text=f"Error Semantico: No se pudo completar un arbol debido a errores de semantica en el código")
        else:
            try:
                tokens = gas.leer_tokens()
                if not tokens:
                    lbl_mensaje.config(text="Error: No se encontraron tokens para analizar.")
                    return
                
                lbl_mensaje.config(text="Construyendo árbol de sintaxis abstracta...")
                semantico.update()
                
                arbol = gas.construir_ast(tokens)
                
                if not arbol:
                    lbl_mensaje.config(text="Error: No se pudo construir el árbol sintáctico.")
                    return
                
                lbl_mensaje.config(text="Generando visualización del árbol...")
                semantico.update()
                
                # Generar la imagen del AST
                imagen_ast = gas.generar_grafico_ast(arbol, "add")
                
                if not imagen_ast or not os.path.exists(imagen_ast):
                    lbl_mensaje.config(text="Error: No se pudo generar la imagen del árbol sintáctico.")
                    return
                
                # Mostrar la imagen del AST
                lbl_mensaje.pack_forget()  # Ocultar el mensaje
                
                try:
                    # Cargar y mostrar la imagen generada
                    img = Image.open(imagen_ast)
                    
                    # Ajustar el tamaño de la imagen manteniendo la proporción
                    width, height = img.size
                    max_width = 850
                    max_height = 650
                    
                    if width > max_width or height > max_height:
                        ratio = min(max_width / width, max_height / height)
                        new_width = int(width * ratio)
                        new_height = int(height * ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    img_tk = ImageTk.PhotoImage(img)
                    
                    # Crear un canvas para mostrar la imagen con scrollbars
                    canvas = tk.Canvas(mensaje_frame, bg="white")
                    scrollbar_y = tk.Scrollbar(mensaje_frame, orient="vertical", command=canvas.yview)
                    scrollbar_x = tk.Scrollbar(mensaje_frame, orient="horizontal", command=canvas.xview)
                    
                    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
                    
                    scrollbar_y.pack(side="right", fill="y")
                    scrollbar_x.pack(side="bottom", fill="x")
                    canvas.pack(side="left", fill="both", expand=True)
                    
                    # Añadir la imagen al canvas
                    canvas.create_image(0, 0, anchor="nw", image=img_tk)
                    canvas.image = img_tk  # Mantener una referencia
                    
                    # Configurar el área de scroll
                    canvas.configure(scrollregion=canvas.bbox("all"))
                    
                except Exception as e:
                    lbl_mensaje.config(text=f"Error al cargar la imagen: {str(e)}")
                    lbl_mensaje.pack(pady=10)
            
            except Exception as e:
                lbl_mensaje.config(text=f"Error en el análisis semantico: {str(e)}")
        
            messagebox.showinfo("Analisis Semantico completado", "Se ha completado correctamente el analisis semantico, actualizando la tabla de simbolos.")
            global flagAnalizadorSem
            flagAnalizadorSem=True
        semantico.mainloop()
    else:
        noAEscrito()

#Ventana que muestra la nueva tabla de simbolos mejorada
def NewtablaSimbolos(parent):
    if flagAnalizadorSem:
        # Cerrar la ventana anterior antes de abrir una nueva ventana
        parent.destroy()
        
        # Creamos la ventana principal con un tamaño fijo, título e icono    
        tabla = Tk()
        tabla.title("Tabla de Simbolos")
        tabla.geometry("1200x800")
        tabla.iconbitmap("Img/compilador.ico")
        
        # Colocamos la imagen de fondo de la ventana y la posicionamos
        imagenTabla = PhotoImage(file="Img/fondo_tabla.png")
        fondoTabla = Label(tabla, image=imagenTabla)
        fondoTabla.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Mantener referencia de la imagen para evitar el recolector de basura
        fondoTabla.image = imagenTabla
        
        # Creando mensaje de Bienvenida y posicionandolo
        bienvenida = Label(tabla, text="Tabla de Simbolos", bg="darkseagreen4", fg="black", font=("Arial", 25, "bold"), bd=3, relief="ridge")
        bienvenida.place(x=425, y=100, width=400, height=60)
        
        # Creando un botón para Regresar al Menú principal
        botonRegresar = Button(tabla, text="Volver", command=lambda: analizadorSemantico(tabla), bg="tan4", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
        botonRegresar.place(x=950, y=700, width=150, height=50)
        
        #Se abre el archivo de la tabla de simbolos
        with open("tabla_simbolos.txt", "r", encoding="utf-8") as f:
            contenido = f.read()

        #Patro para leer en el archivo
        #(\d+)\s+(\w+)\s+(\w+)\s+(\w+|[^\s]+)\s+(-|\d+|[^\s]+)\s+(\d+)\s+(0x[0-9a-fA-F]+)
        patron = r"(\d+)\s+(\w+)\s+(\w+)\s+(\w+|[^\s]+|\".+\")\s+(-|-*\d+|-*\d+\.\d+|\"[^\"]+\"|\'[^\s]\')\s+(\d+)\s+(0x[0-9a-fA-F]+)" #r"<(\w+),\s*([^,]+),\s*(\d+)>"
        tokens = re.findall(patron, contenido)
        print(tokens)
        

        #Frame para posicionar la tabla
        moverTabla = Frame(tabla, width=1000 ,height=400)
        # Evita que el marco cambie de tamaño por los elementos que contiene
        moverTabla.pack_propagate(False)
        moverTabla.pack(padx=1, pady=240)

        #Tabla utilizando treeview
        encabezado=["ID","Categoria","Tipo","Lexema","valor", "linea", "Direccion de memoria\n"] 
        tree = ttk.Treeview(moverTabla, columns=encabezado, show="headings", height=400)
        tree.pack()
        #Abrir el archivo de la tabla
        leerTablaSimbolos(tokens, tree, encabezado)
        tree.pack()

        #Scrollbar para ver codigos grandes
        scrollbar = Scrollbar(moverTabla, command=tree.yview, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        tree.config(yscrollcommand=scrollbar.set)
        # Mantenemos la ventana abierta
        tabla.mainloop()
    else:
        messagebox.showerror("Error del Analizador Semantico","No se puede desplegar la nueva tabla hasta que el analizador semantico acepte el código.")
            
#Ventana del Código Intermedio
def codigoIntermedio(parent):
    if flagAnalizadorSem:
        # Cerrar la ventana anterior antes de abrir una nueva ventana
        parent.destroy()
        
        # Creamos la ventana principal con un tamaño fijo, título e icono
        intermedio = Tk()
        intermedio.title("Código Intermedio")
        centrar_ventana(intermedio, 1200, 800)
        intermedio.iconbitmap("Img/compilador.ico")
        
        # Colocamos la imagen de fondo de la ventana y la posicionamos
        imagenIntermedio = PhotoImage(file="Img/fondo_intermedio.png")
        fondoIntermedio = Label(intermedio, image=imagenIntermedio)
        fondoIntermedio.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Mantener referencia de la imagen para evitar el recolector de basura
        fondoIntermedio.image = imagenIntermedio
        
        # Creando mensaje de Bienvenida y posicionándolo
        bienvenida = Label(intermedio, text="Código Intermedio", bg="papayawhip", fg="black", font=("Arial", 25, "bold"), bd=3, relief="ridge")
        bienvenida.place(x=425, y=100, width=400, height=60)
        
        # Botón para regresar al menú principal
        botonRegresar = Button(intermedio, text="Volver", command=lambda: principal(intermedio), bg="navajowhite4", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
        botonRegresar.place(x=950, y=700, width=150, height=50)
        
        # Botón para guardar el código intermedio
        botonGuardar = Button(intermedio, text="Guardar Código", command=lambda: guardar_codigo_intermedio_ui(tac_generator), bg="papayawhip", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
        botonGuardar.place(x=700, y=700, width=225, height=50)
        
        # Crear un frame para mostrar el código intermedio
        mensaje_frame = Frame(intermedio, bg="white", bd=4, relief="ridge")
        mensaje_frame.place(x=150, y=200, width=900, height=475)
        
        # Etiqueta para mostrar mensajes
        lbl_mensaje = Label(mensaje_frame, text="Generando código intermedio...", bg="white", font=("Arial", 14))
        lbl_mensaje.pack(pady=10)
        
        try:
            # Importar el módulo de código intermedio
            import generador_codigo_intermedio as gci
            
            # Generar el código intermedio
            tokens = gci.leer_tokens()
            if not tokens:
                lbl_mensaje.config(text="Error: No se encontraron tokens para analizar.")
                return
            
            lbl_mensaje.config(text="Construyendo árbol de sintaxis abstracta...")
            intermedio.update()
            
            # Utilizar el árbol generado por el analizador semántico
            ast = gas.construir_ast(tokens)
            if not ast:
                lbl_mensaje.config(text="Error: No se pudo construir el árbol sintáctico.")
                return
            
            lbl_mensaje.config(text="Generando código intermedio...")
            intermedio.update()
            
            # Generar el código intermedio
            tac_generator = gci.generar_codigo_intermedio(ast)
            if not tac_generator:
                lbl_mensaje.config(text="Error: No se pudo generar el código intermedio.")
                return
            
            # Obtener el código intermedio como texto
            codigo_tac = tac_generator.get_code_as_string()
            
            # Guardar el código en un archivo
            gci.guardar_codigo_intermedio(tac_generator)
            
            # Generar visualización gráfica
            lbl_mensaje.config(text="Generando visualización gráfica...")
            intermedio.update()
            
            imagen_tac = gci.generar_grafico_tac(tac_generator, "tac_graph")
            
            # Mostrar el código y la visualización
            lbl_mensaje.pack_forget()
            
            # Frame con pestañas para mostrar código y gráfico
            notebook = ttk.Notebook(mensaje_frame)
            notebook.pack(fill='both', expand=True)
            
            # Pestaña de código
            tab_codigo = Frame(notebook)
            notebook.add(tab_codigo, text="Código de Tres Direcciones")
            
            # Crear un widget de texto para mostrar el código
            texto_codigo = Text(tab_codigo, wrap=WORD, font=("Courier New", 12))
            texto_codigo.insert("1.0", codigo_tac)
            texto_codigo.config(state=DISABLED)
            
            # Añadir scrollbars
            scrollbar_y = Scrollbar(tab_codigo, orient="vertical", command=texto_codigo.yview)
            scrollbar_x = Scrollbar(tab_codigo, orient="horizontal", command=texto_codigo.xview)
            texto_codigo.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")
            texto_codigo.pack(side="left", fill="both", expand=True)
            
            # Pestaña de gráfico (si se generó)
            if imagen_tac and os.path.exists(imagen_tac):
                tab_grafico = Frame(notebook)
                notebook.add(tab_grafico, text="Visualización Gráfica")
                
                try:
                    # Cargar y mostrar la imagen generada
                    img = Image.open(imagen_tac)
                    
                    # Ajustar el tamaño de la imagen manteniendo la proporción
                    width, height = img.size
                    max_width = 850
                    max_height = 450
                    
                    if width > max_width or height > max_height:
                        ratio = min(max_width / width, max_height / height)
                        new_width = int(width * ratio)
                        new_height = int(height * ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    img_tk = ImageTk.PhotoImage(img)
                    
                    # Crear un canvas para mostrar la imagen con scrollbars
                    canvas = Canvas(tab_grafico, bg="white")
                    scrollbar_y_img = Scrollbar(tab_grafico, orient="vertical", command=canvas.yview)
                    scrollbar_x_img = Scrollbar(tab_grafico, orient="horizontal", command=canvas.xview)
                    
                    canvas.configure(yscrollcommand=scrollbar_y_img.set, xscrollcommand=scrollbar_x_img.set)
                    
                    scrollbar_y_img.pack(side="right", fill="y")
                    scrollbar_x_img.pack(side="bottom", fill="x")
                    canvas.pack(side="left", fill="both", expand=True)
                    
                    # Añadir la imagen al canvas
                    canvas.create_image(0, 0, anchor="nw", image=img_tk)
                    canvas.image = img_tk  # Mantener una referencia
                    
                    # Configurar el área de scroll
                    canvas.configure(scrollregion=canvas.bbox("all"))
                    
                except Exception as e:
                    Label(tab_grafico, text=f"Error al cargar la imagen: {str(e)}", bg="white", font=("Arial", 12)).pack(pady=10)
            
            messagebox.showinfo("Generación exitosa", "El código intermedio se ha generado correctamente.")
            
        except Exception as e:
            lbl_mensaje.config(text=f"Error en la generación de código intermedio: {str(e)}")
        
        intermedio.mainloop()
    else:
        messagebox.showerror("Error del Analizador Semántico", "No se puede generar código intermedio hasta que el analizador semántico acepte el código.")

# Función para guardar el código intermedio desde la interfaz
def guardar_codigo_intermedio_ui(tac_generator):
    """Guarda el código intermedio en la ubicación que elija el usuario."""
    from tkinter import filedialog
    
    # Abrir diálogo para seleccionar dónde guardar
    ruta_destino = filedialog.asksaveasfilename(
        defaultextension=".tac",
        filetypes=[("Three Address Code", "*.tac"), ("Text files", "*.txt"), ("All files", "*.*")],
        title="Guardar código intermedio"
    )
    
    if ruta_destino:
        try:
            # Guardar el código en el destino seleccionado
            import generador_codigo_intermedio as gci
            success = gci.guardar_codigo_intermedio(tac_generator, ruta_destino)
            if success:
                messagebox.showinfo("Éxito", "Código intermedio guardado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo guardar el código intermedio.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el código: {str(e)}")

# Creamos la ventana para la función de optimizar código intermedio
def optimizarCodigo(parent):

    if not flagAnalizadorSem: #Verificamos que se haya realizado el analisis semantico previamente
        noAEscrito()
        return

    parent.destroy()

    optimizador = Tk()
    optimizador.title("Código Optimizado")
    centrar_ventana(optimizador, 1200, 850)
    optimizador.iconbitmap("Img/compilador.ico")

    imagenFondo = PhotoImage(file="Img/fondo_optimizacion.png")
    fondo = Label(optimizador, image=imagenFondo)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    fondo.image = imagenFondo

    Label(optimizador, text="Código Optimizado", bg="LightSteelBlue4", fg="black", font=("Arial", 25, "bold"), bd=3, relief="ridge").place(x=325, y=20, width=600, height=60)

    # TextArea para el código
    text_area = Text(optimizador, font=("Courier", 12), wrap=NONE)
    text_area.place(x=50, y=90, width=1100, height=300)
    scrollbar_y = Scrollbar(optimizador, command=text_area.yview)
    scrollbar_y.place(x=1150, y=90, height=300)
    text_area.config(yscrollcommand=scrollbar_y.set)

    # Imagen del TAC optimizado
    image_label = Label(optimizador, bg="white", bd=2, relief="solid")
    image_label.place(x=300, y=420, width=600, height=300)

    # Variables para zoom
    zoom_factor = [1.0]
    original_image = [None]

    # Funciones de zoom
    def actualizar_imagen():
        if original_image[0]:
            img = original_image[0]
            width, height = img.size
            new_size = (int(width * zoom_factor[0]), int(height * zoom_factor[0]))
            resized = img.resize(new_size, Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(resized)
            image_label.config(image=img_tk)
            image_label.image = img_tk

    def zoom_in():
        zoom_factor[0] += 0.1
        actualizar_imagen()

    def zoom_out():
        zoom_factor[0] = max(0.1, zoom_factor[0] - 0.1)
        actualizar_imagen()

    def guardar_imagen():
        if original_image[0]:
            ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
            if ruta:
                original_image[0].save(ruta)
                messagebox.showinfo("Guardado", "Imagen guardada correctamente.")

    # Generar y mostrar TAC optimizado
    tac_generator = generar_codigo_intermedio()
    if tac_generator:
        tac_generator = optimizar_codigo_intermedio(tac_generator)
        codigo_opt = tac_generator.get_code_as_string()
        text_area.insert("1.0", codigo_opt)

        with open("codigo_optimizado.txt", "w", encoding="utf-8") as f:
            f.write(codigo_opt)

        ruta_img = generar_grafico_tac(tac_generator, "codigo_optimizado")

        if ruta_img and os.path.exists(ruta_img):
            img = Image.open(ruta_img)
            original_image[0] = img
            actualizar_imagen()

        messagebox.showinfo("Optimización completa", "Código optimizado y graficado exitosamente.")
    else:
        text_area.insert("1.0", "Error generando el código intermedio.")

    # Botones
    Button(optimizador, text="Zoom +", command=zoom_in, font=("Arial", 20, "bold"), bg="black", fg="white", bd=4, relief="raised").place(x=250, y=730, width=150, height=50)
    Button(optimizador, text="Zoom -", command=zoom_out, font=("Arial", 20, "bold"), bg="black", fg="white", bd=4, relief="raised").place(x=525, y=730, width=150, height=50)
    Button(optimizador, text="Guardar", command=guardar_imagen, font=("Arial", 20, "bold"), bg="black", fg="white", bd=4, relief="raised").place(x=800, y=730, width=150, height=50)
    Button(optimizador, text="Volver", command=lambda: principal(optimizador), font=("Arial", 20, "bold"), bg="black", fg="white", bd=4, relief="raised").place(x=1000, y=750, width=150, height=50)

    optimizador.mainloop()

    
def generarCodigo(parent):
    if not os.path.exists('codigo_origen.txt'):
        messagebox.showerror("Error", "No se ha generado el código intermedio.")
        return
    
    #Cerramos la ventana que está abierta
    parent.destroy()
    
    #Creamos la ventanan de generación de código
    generacion = Tk()
    generacion.title("Generación de Código")
    centrar_ventana(generacion, 1200, 800)
    generacion.iconbitmap("Img/compilador.ico")
    
    # Colocamos la imagen de fondo de la ventana y la posicionamos
    imagen_generacion = PhotoImage(file="Img/fondo_generacion.png")
    fondo_generacion = Label(generacion, image=imagen_generacion)
    fondo_generacion.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Mantener referencia de la imagen para evitar el recolector de basura
    fondo_generacion.image = imagen_generacion
    
    # Creamos un mensaje de bienvenida
    bienvenida = Label(generacion, text="Generación de Código Intermedio", bg="HotPink4", fg="black", font=("Arial", 25, "bold"), bd=3, relief="raised")
    bienvenida.place(x=300, y=100, width=600, height=60)
    
    botonRegresar = tk.Button(generacion, text="Volver", command=lambda: principal(generacion), bg="gray12", fg="white", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonRegresar.place(x=950, y=700, width=150, height=50)

    #Cuadro con su scrollbar para ver el codigo transformado de .tac a .asm
    asm_code = Text(generacion, width=90, height=20, font=("Arial", 14, "bold"), wrap="word")
    asm_code.place(x=100, y=200)
    #Scrollbar para ver codigos grandes
    scrollbar = Scrollbar(generacion, command=asm_code.yview)
    scrollbar.pack(side="right", fill='y')

    asm_code.config(yscrollcommand=scrollbar.set)

    #Generar el archivo ASM si existe el archivo TAC
    asm = compi.convertir_tac_a_asm("codigo_intermedio")
    #Boton para compilar el programa segun la posicion que desee el usuario
    botonRegresar = tk.Button(generacion, text="Volver", command=lambda: principal(generacion), bg="gray12", fg="white", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonRegresar.place(x=950, y=700, width=150, height=50)

    if "ERROR:" in asm:
        asm_code.insert('1.0', "NO SE PUEDO GENERAR EL ARCHIVO ASM\n\n")
        messagebox.showerror("Error en la generación", asm)
    else:#Si todo esta en orden el programa permite que se pueda compilar el codigo
        #Se imprime en el Text el archivo ASM
        
        #Boton para compilar el programa
        botonComp = tk.Button(generacion, text="Compilar", command=CompilarCode, bg="HotPink4", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
        botonComp.place(x=650, y=700, width=150, height=50)
        messagebox.showinfo("Generacion Exitosa", "Se ha generado el archivo .asm correctamente.")
    asm_code.insert('1.0', asm)
    asm_code.config(state=DISABLED)

def CompilarCode():

    ruta_archivo = filedialog.asksaveasfilename(
        title="Guardar archivo",
        defaultextension=".exe",
        filetypes=[("Archivos de texto", "*.exe")]
    )

    if ruta_archivo:  # Si el usuario selecciona una ruta

        dir = os.path.dirname(ruta_archivo)
        nombre = os.path.basename(ruta_archivo).strip().replace(".exe", "")
        compi.compilar(nombre, dir)
        messagebox.showinfo("Compilacion Exitosa", f"Se a generado el ejecutable de su programa \"{nombre}\"")
    else:
        return


# Creamos la ventana para la ejecución del código 
def ejecutarCodigo(parent):
    if not os.path.exists('codigo_origen.txt'):
        messagebox.showerror("Error", "No se ha generado el código intermedio.")
        return
    
    # Cerramos la ventana que esté abierta
    parent.destroy()
    
    # Creamos la ventana de ejecución
    ejecucion = Tk()
    ejecucion.title("Ejecución de Código")
    centrar_ventana(ejecucion, 1200, 800)
    ejecucion.iconbitmap("Img/compilador.ico")
    
    # Colocamos la imagen de fondo de la ventana y la posicionamos
    imagen_ejecucion = PhotoImage(file="Img/fondo_ejecucion.png")
    fondo_ejecucion = Label(ejecucion, image=imagen_ejecucion)
    fondo_ejecucion.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Mantener referencia de la imagen para evitar el recolector de basura
    fondo_ejecucion.image = imagen_ejecucion
    
    # Creamos un mensaje de bienvenida
    bienvenida = Label(ejecucion, text="Ejecución de Código Intermedio", bg="AntiqueWhite3", fg="black", font=("Arial", 25, "bold"), bd=3, relief="raised")
    bienvenida.place(x=300, y=100, width=600, height=60)
    
    botonRegresar = tk.Button(ejecucion, text="Volver", command=lambda: principal(ejecucion), bg="NavajoWhite3", fg="black", font=("Arial", 20, "bold"), bd=4, relief="raised")
    botonRegresar.place(x=950, y=700, width=150, height=50)

# Inicializamos Pygame para gestionar el sonido  
pygame.init()  
pygame.mixer.init()  

# Cargamos el sonido  
try:  
    pygame.mixer.music.load("Sonido/sonido_carga.wav")  # Cambia esta ruta según la ubicación de tu archivo  
except pygame.error as e:  
    print(f"No se pudo cargar el sonido: {e}")  

def animacion(fotogramaActual=0):  
    global ciclo  
    cargaImagen = fotogramasImagen[fotogramaActual]  
    
    gifCarga.config(image=cargaImagen)  
    fotogramaActual = fotogramaActual + 1  
    
    if fotogramaActual == len(fotogramasImagen):  
        fotogramaActual = 0  
    
    ciclo = carga.after(70, lambda: animacion(fotogramaActual))  

# Función para parar la animación de carga  
def pararAnimacion():  
    carga.after_cancel(ciclo)  

def limpiar_proyecto():
    """
    Limpia todos los archivos generados por el compilador.
    Elimina archivos de tokens, tabla de símbolos, código intermedio,
    imágenes de árboles sintácticos y archivos temporales.
    """
    import os
    import glob
    import tkinter as tk
    from tkinter import messagebox
    
    # Lista de archivos específicos a eliminar
    archivos_especificos = [
        "codigo_origen.txt",
        "tokens.txt",
        "tabla_simbolos.txt",
        "codigo_intermedio.tac",
        "codigo_optimizado.txt",
        "tabla_simbolos_variables.txt"
    ]
    
    # Patrones de archivos a eliminar
    patrones = [
        "*.png",  # Imágenes generadas
        "*.dot",  # Archivos dot de graphviz
        "ast.*",  # Archivos del árbol sintáctico
        "add.*",  # Archivos del árbol semántico
        "tac_graph.*"  # Archivos del grafo de código intermedio
    ]
    
    archivos_eliminados = 0
    
    # Eliminar archivos específicos
    for archivo in archivos_especificos:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                archivos_eliminados += 1
                print(f"Archivo eliminado: {archivo}")
            except Exception as e:
                print(f"Error al eliminar {archivo}: {str(e)}")
    
    # Eliminar archivos que coincidan con los patrones
    for patron in patrones:
        for archivo in glob.glob(patron):
            try:
                os.remove(archivo)
                archivos_eliminados += 1
                print(f"Archivo eliminado: {archivo}")
            except Exception as e:
                print(f"Error al eliminar {archivo}: {str(e)}")
    
    # Restablecer variables globales en el archivo main.py
    global texto_ingresado
    global strTokens
    global flagAnalizadorSem
    
    texto_ingresado = ""
    strTokens = ""
    flagAnalizadorSem = False
    
    # Mostrar mensaje de éxito
    messagebox.showinfo("Limpieza completada", f"Se han eliminado {archivos_eliminados} archivos.\nPuedes ingresar un nuevo código para compilar.")
    
    return archivos_eliminados


def nuevo_proyecto(editor_ventana, text_widget):
    """
    Limpia todos los archivos generados y el editor de texto para comenzar un nuevo proyecto.
    
    Args:
        editor_ventana: La ventana del editor de texto
        text_widget: El widget de texto a limpiar
    """
    # Preguntar al usuario si está seguro
    respuesta = messagebox.askyesno("Nuevo Proyecto", 
                                    "¿Estás seguro de que deseas comenzar un nuevo proyecto?\n\nSe eliminarán todos los archivos generados y el código actual.")
    
    if respuesta:
        # Limpiar el editor de texto
        text_widget.delete("1.0", END)
        
        # Limpiar los archivos del proyecto
        archivos_eliminados = limpiar_proyecto()
        
        # Mensaje adicional específico para el editor
        messagebox.showinfo("Editor Limpio", "El editor ha sido limpiado.\nPuedes comenzar a escribir tu nuevo código.")


def centrar_ventana(ventana, ancho, alto):
    """
    Centra una ventana en la pantalla.
    
    Args:
        ventana: La ventana de Tkinter a centrar
        ancho: Ancho de la ventana
        alto: Alto de la ventana
    """
    # Obtener el ancho y alto de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    # Calcular la posición x, y para centrar la ventana
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    
    # Configurar la geometría de la ventana
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    # Opcional: impedir que la ventana sea redimensionada
    # ventana.resizable(False, False)

# Presentamos una ventana de carga  
carga = Tk()  
carga.title("Cargando...")  
centrar_ventana(carga, 692, 388)
carga.iconbitmap("Img/carga.ico")  

# Creando Animación de Gif para pantalla de Carga  
archivoCarga = "Img/cargando.gif"  
gifImagen = Image.open(archivoCarga)  

fotogramasImagen = []  
try:  
    while True:  
        fotograma = ImageTk.PhotoImage(gifImagen.copy())  
        fotogramasImagen.append(fotograma)  
        gifImagen.seek(len(fotogramasImagen))  # Ir al siguiente fotograma  
except EOFError:  
    pass  # Alcanzamos el final del GIF  

gifCarga = Label(carga, image="")  
gifCarga.pack()  

# Iniciar la animación del GIF  
carga.after(0, animacion)  # Tiempo en milisegundos, función a la que llama  

# Iniciar el sonido de carga  
pygame.mixer.music.play() 

# Llamamos a la función que abre la ventana principal después de 7000 ms  
carga.after(7000, lambda: principal(carga))  

# Comprobar si ya hay código guardado para escribirlo en el editor de texto  
if os.path.exists(archiCodBase):  
    texto_ingresado = leerArchivo(archiCodBase)  
    analizador = gram.analizadorLex(texto_ingresado)  # Almacena temporalmente el resultado del analizador léxico  
    if analizador == -1:  # Si hay un símbolo que no se reconoce  
        texto_ingresado = ""  
        messagebox.showwarning('Advertencia', 'Se ha detectado un símbolo que no reconoce la gramática en el archivo')  
    else:  
        lexer = analizador  
        strTokens = leerArchivo(archiTokens)  

# Detener el sonido después de que finalice el tiempo de carga  
carga.after(7000, pygame.mixer.music.stop)  

# Mantenemos la ventana abierta  
carga.mainloop()  

# Finalizamos Pygame  
pygame.quit()  