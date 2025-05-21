import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import ply.gramatica as grammar
import ply.analisis_semantico_operadores as an
import ply.lex as lex
import os
import re
import graphviz
import pygame

newTokens = []

def generarToken(tabla):
    with open(tabla, "r", encoding="utf-8") as f:
            contenido = f.read()

    #Patro para leer en el archivo
    patron = r"(\d+)\s+(\w+)\s+(\w+)\s+(\w+|[^\s]+|\".+\")\s+(-|\d+|\"[^\"]+\"|\'[^\s]\')\s+(\d+)\s+(0x[0-9a-fA-F]+)" #r"<(\w+),\s*([^,]+),\s*(\d+)>"
    tokens = re.findall(patron, contenido)
    global newTokens
    newTokens=[]

    for id, cat, tipo, lex, val, linea, dir in tokens:
        if cat=='VAR' or cat in ['NUMBER', 'FLOATING', 'FLOAT', 'RESERV','CHAR', 'STRING']:
          token = [cat,tipo,lex,linea]
        else:
          token = [cat,cat,lex,linea]
        newTokens.append(token)
        #print(token)
    return newTokens

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
        
        elif token_type == "RESERV" and token_value == "else":
            return parse_else_statement()
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
            expression = parse_dec_assignment()
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

        print(tokens[index[0]])
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
    def parse_else_statement():
        index[0]+=1
        el_nodo = ASTNode("ELSE", None, None, None)

        # Consumir '{'
        if index[0] < len(tokens) and tokens[index[0]][0] == "RLLAVE":
            index[0] += 1
        else:
            return None  # Error: esperaba '{'
        
        block_statements = []
        while index[0] < len(tokens) and tokens[index[0]][0] != "LLLAVE":
            stmt = parse_statement()
            if stmt:
                block_statements.append(stmt)
        
        # Crear nodo de bloque
        if len(block_statements) > 0:
            block_node = ASTNode("BLOCK", None, block_statements, None)
            el_nodo.derecho = block_node
        
        # Consumir '}'
        if index[0] < len(tokens) and tokens[index[0]][0] == "LLLAVE":
            index[0] += 1

        return el_nodo 
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
        
        # Consumir '}do;'
        if index[0] < len(tokens) and tokens[index[0]][0] == "LLLAVE":
            index[0] += 1
            if index[0] < len(tokens) and tokens[index[0]][0]=="RESERV" and tokens[index[0]][1] == "do":
                index[0] += 1
                if index[0] < len(tokens) and tokens[index[0]][0] == "POINTCOMA":
                    index[0] += 1
                else:
                    return None
            else:
                return None
        else:
            return None
        
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
    #fucnion para inicializar una variable
    def parse_dec_assignment():
        """Parsea una asignación:  = expresión;"""
        print(tokens[index[0]][0])
        if index[0] >= len(tokens) or tokens[index[0]][0] != "EQUAL":
            return None  # Error: esperaba '='
        
        index[0] += 1  # Consumir el '='
        expression = parse_expression()
        # Crear nodo de asignación
        assignment_node = ASTNode("ASSIGNMENT", "=", None, expression)
        
        # Consumir punto y coma
        if index[0] < len(tokens) and tokens[index[0]][0] == "POINTCOMA":
            index[0] += 1
            
        return assignment_node
    
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
        
        while index[0] < len(tokens) and tokens[index[0]][0] in ["MAYOR", "MENOR", "MAEQUAL", "MEEQUAL", "EQUAL", "DOBLEEQUAL"]:
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
        left = parse_factor()
        
        while index[0] < len(tokens) and tokens[index[0]][0] in ["MULT", "DIV"]:
            op_token = tokens[index[0]]
            index[0] += 1  # Consumir el operador
            
            right = parse_factor()
            
            # Crear nodo multiplicativo
            left = ASTNode("MULTIPLICATIVE", op_token[1], left, right)
        
        return left
    
    def parse_factor():
        tipo = tokens[index[0]][0]
        factor = ASTNode("FACTOR", tipo, parse_primary(), None)
        return factor
    
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

#tokens=generarToken("tabla_simbolos.txt")
tokens=leer_tokens()
arbol = construir_ast(tokens)