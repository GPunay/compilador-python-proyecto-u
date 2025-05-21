"""
Módulo generador de código intermedio para el compilador.
Este módulo implementa la generación de código de tres direcciones.
"""

import re
import os
import graphviz
from generar_arbolSem import ASTNode, leer_tokens, construir_ast

# Clase para representar instrucciones de tres direcciones
class TACInstruction:
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    
    def __str__(self):
        if self.op == "LABEL":
            return f"{self.result}:"
        elif self.op == "GOTO":
            return f"goto {self.result}"
        elif self.op == "IF":
            return f"if {self.arg1} goto {self.result}"
        elif self.op == "IFFALSE":
            return f"ifFalse {self.arg1} goto {self.result}"
        elif self.op in ["=", "ASSIGN"]:
            if self.arg2 is None:
                return f"{self.result} = {self.arg1}"
            else:
                return f"{self.result} = {self.arg1}"
        elif self.op == "CALL":
            return f"{self.result} = call {self.arg1}"
        elif self.op == "PRINT":
            return f"print {self.arg1}"
        elif self.op == "RETURN":
            return f"return {self.arg1}"
        else:
            # Operaciones binarias
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"

# Generador de código de tres direcciones
class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        """Crea un nuevo nombre temporal."""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        """Crea una nueva etiqueta."""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, op, arg1=None, arg2=None, result=None):
        """Emite una instrucción TAC."""
        instr = TACInstruction(op, arg1, arg2, result)
        self.instructions.append(instr)
        return instr
    
    def generate_code_from_ast(self, node):
        """
        Genera código de tres direcciones a partir de un AST.
        
        Args:
            node: Nodo raíz del árbol AST.
            
        Returns:
            Nombre del último valor temporal o literal generado.
        """
        print("Tipo del nodo" + str(node.valor))
        print(node.tipo)
        if node is None:
            return None
        
        # Maneja diferentes tipos de nodos
        if node.tipo == "PROGRAM":
            # Para un programa, genera código para cada declaración
            for stmt in node.izquierdo:
                self.generate_code_from_ast(stmt)
            return None
            
        elif node.tipo == "NUMBER" or node.tipo == "CHAR" or node.tipo == "BOOL" or node.tipo == "STRING":
            # Para literales, simplemente devuelve el valor
            return node.valor
            
        elif node.tipo == "VAR":
            # Para variables, devuelve el nombre
            return node.valor
        
        elif node.tipo == "FACTOR":
            # Para factores, procesa el hijo izquierdo
            if node.izquierdo:
                return self.generate_code_from_ast(node.izquierdo)
            return None
            
        elif node.tipo == "DECLARATION":
            # Para declaraciones, emite una asignación si hay un valor inicial
            var_name = node.izquierdo.valor
            if node.derecho:
                expr_result = self.generate_code_from_ast(node.derecho)
                self.emit("=", expr_result, None, var_name)
            return None
            
        elif node.tipo == "ASSIGNMENT":
            # Para asignaciones, emite una instrucción de asignación
            if node.izquierdo and node.izquierdo.tipo == "VAR":
                var_name = node.izquierdo.valor
                expr_result = self.generate_code_from_ast(node.derecho)
                self.emit("=", expr_result, None, var_name)
                return var_name
            elif node.derecho:
                # Si no tiene izquierdo (como en una declaración con inicialización)
                expr_result = self.generate_code_from_ast(node.derecho)
                return expr_result
            return None
            
        elif node.tipo == "ADDITIVE" or node.tipo == "MULTIPLICATIVE":
            # Para operaciones binarias, genera código para ambos operandos
            # y emite una instrucción para la operación
            left_result = self.generate_code_from_ast(node.izquierdo)
            right_result = self.generate_code_from_ast(node.derecho)
            temp = self.new_temp()
            self.emit(node.valor, left_result, right_result, temp)
            return temp
            
        elif node.tipo == "COMPARISON":
            # Para comparaciones, genera código de manera similar a las operaciones binarias
            left_result = self.generate_code_from_ast(node.izquierdo)
            right_result = self.generate_code_from_ast(node.derecho)
            temp = self.new_temp()
            op_map = {
                ">": ">",
                "<": "<",
                ">=": ">=",
                "<=": "<=",
                "==": "==",
                "!=": "!="
            }
            op = op_map.get(node.valor, node.valor)
            self.emit(op, left_result, right_result, temp)
            return temp
            
        elif node.tipo == "IF":
            # Para sentencias if, genera código para la condición,
            # y luego para el bloque then (y el bloque else si existe)
            condition_result = self.generate_code_from_ast(node.izquierdo)
            
            # Etiquetas para saltos
            else_label = self.new_label()
            end_label = self.new_label()
            
            # Salta a else si la condición es falsa
            self.emit("IFFALSE", condition_result, None, else_label)
            
            # Genera código para el bloque then
            if node.derecho:
                if isinstance(node.derecho, list):
                    for stmt in node.derecho:
                        self.generate_code_from_ast(stmt)
                else:
                    self.generate_code_from_ast(node.derecho)
             
            # Salta al final después del bloque then
            self.emit("GOTO", None, None, end_label)
            
            # Etiqueta para el bloque else
            self.emit("LABEL", None, None, else_label)
            
            # Código para el bloque else (si existe)
            # Nota: El AST proporcionado no tiene una estructura explícita para else
            
            # Etiqueta para el final del if
            self.emit("LABEL", None, None, end_label)
            
            return None
            
        elif node.tipo == "WHILE":
            # Para bucles while, genera código similar a if, pero con un salto
            # de vuelta al inicio del bucle
            
            # Etiqueta para el inicio del bucle
            start_label = self.new_label()
            self.emit("LABEL", None, None, start_label)
            
            # Evaluar la condición
            condition_result = self.generate_code_from_ast(node.izquierdo)
            
            # Etiqueta para el final del bucle
            end_label = self.new_label()
            
            # Salta al final si la condición es falsa
            self.emit("IFFALSE", condition_result, None, end_label)
            
            # Genera código para el cuerpo del bucle
            if node.derecho:
                if isinstance(node.derecho, list):
                    for stmt in node.derecho:
                        self.generate_code_from_ast(stmt)
                else:
                    self.generate_code_from_ast(node.derecho)
            
            # Salta de vuelta al inicio
            self.emit("GOTO", None, None, start_label)
            
            # Etiqueta para el final del bucle
            self.emit("LABEL", None, None, end_label)
            
            return None
        
        elif node.tipo == "ELSE":
            # Para bloques else, genera código para el cuerpo
            if node.derecho:
                if isinstance(node.derecho, list):
                    for stmt in node.derecho:
                        self.generate_code_from_ast(stmt)
                else:
                    self.generate_code_from_ast(node.derecho)
            return None
            
        elif node.tipo == "PRINT":
            # Para sentencias print, genera código para la expresión
            # y emite una instrucción print
            expr_result = self.generate_code_from_ast(node.izquierdo)
            self.emit("PRINT", expr_result, None, None)
            return None
            
        elif node.tipo == "BLOCK":
            # Para bloques de código, genera código para cada sentencia
            if isinstance(node.izquierdo, list):
                for stmt in node.izquierdo:
                    self.generate_code_from_ast(stmt)
            else:
                self.generate_code_from_ast(node.izquierdo)
            return None
            
        else:
            # Tipo de nodo desconocido
            print(f"Tipo de nodo no manejado: {node.tipo}")
            return None


    def get_code(self):
        """Devuelve el código TAC como una lista de cadenas."""
        return [str(instr) for instr in self.instructions]
    
    def get_code_as_string(self):
        """Devuelve el código TAC como una sola cadena."""
        return "\n".join(self.get_code())

class TACOptimizer:
    """
    Optimizador de código de tres direcciones.
    Implementa diversas técnicas de optimización para mejorar
    la eficiencia del código generado.
    """
    def __init__(self, tac_generator):
        self.tac_generator = tac_generator
        self.instructions = tac_generator.instructions.copy()
        # Mapeo para la propagación de copias
        self.copy_map = {}
        # Conjunto de variables utilizadas
        self.used_vars = set()
        # Mapeo de etiquetas a índices
        self.label_map = {}
        self._build_label_map()
    
    def _build_label_map(self):
        """Construye un mapeo de etiquetas a índices de instrucciones."""
        for i, instr in enumerate(self.instructions):
            if instr.op == "LABEL":
                self.label_map[instr.result] = i
    
    def optimize(self):
        """Aplica todas las optimizaciones disponibles."""
        self._mark_used_variables()
        self._constant_folding()
        self._algebraic_simplification()
        self._copy_propagation()
        self._dead_code_elimination()
        self._jump_optimization()
        return self.instructions
    
    def _mark_used_variables(self):
        """Marca todas las variables utilizadas en el código."""
        # Primera pasada: marcar variables utilizadas en la parte derecha
        for instr in self.instructions:
            if instr.op in ["PRINT", "IF", "IFFALSE"]:
                if instr.arg1 and not instr.arg1.startswith('t') and not self._is_literal(instr.arg1):
                    self.used_vars.add(instr.arg1)
            elif instr.op not in ["LABEL", "GOTO"]:
                if instr.arg1 and not self._is_literal(instr.arg1):
                    self.used_vars.add(instr.arg1)
                if instr.arg2 and not self._is_literal(instr.arg2):
                    self.used_vars.add(instr.arg2)
        
        # Segunda pasada: propagar hacia atrás desde las variables utilizadas
        changed = True
        while changed:
            changed = False
            for instr in self.instructions:
                if instr.op != "LABEL" and instr.result:
                    if instr.result in self.used_vars:
                        if instr.arg1 and not self._is_literal(instr.arg1):
                            if instr.arg1 not in self.used_vars:
                                self.used_vars.add(instr.arg1)
                                changed = True
                        if instr.arg2 and not self._is_literal(instr.arg2):
                            if instr.arg2 not in self.used_vars:
                                self.used_vars.add(instr.arg2)
                                changed = True
    
    def _is_literal(self, value):
        """Determina si un valor es una literal (número, cadena, etc.)."""
        if value is None:
            return True
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            if isinstance(value, str) and (value.startswith('"') or value.startswith("'")):
                return True
            return False
    
    def _constant_folding(self):
        """Evalúa expresiones constantes en tiempo de compilación."""
        for i, instr in enumerate(self.instructions):
            if instr.op in ["+", "-", "*", "/", "%", ">", "<", ">=", "<=", "==", "!="]:
                # Comprobar si ambos operandos son constantes
                if self._is_literal(instr.arg1) and self._is_literal(instr.arg2):
                    try:
                        # Convertir a números si es posible
                        a = float(instr.arg1)
                        b = float(instr.arg2)
                        
                        # Evaluar la expresión
                        result = None
                        if instr.op == "+":
                            result = a + b
                        elif instr.op == "-":
                            result = a - b
                        elif instr.op == "*":
                            result = a * b
                        elif instr.op == "/":
                            if b != 0:
                                result = a / b
                        elif instr.op == "%":
                            if b != 0:
                                result = a % b
                        elif instr.op == ">":
                            result = a > b
                        elif instr.op == "<":
                            result = a < b
                        elif instr.op == ">=":
                            result = a >= b
                        elif instr.op == "<=":
                            result = a <= b
                        elif instr.op == "==":
                            result = a == b
                        elif instr.op == "!=":
                            result = a != b
                        
                        if result is not None:
                            # Convertir de nuevo a entero si es posible
                            if result == int(result):
                                result = int(result)
                            
                            # Reemplazar la instrucción por una asignación constante
                            self.instructions[i] = type(instr)("=", str(result), None, instr.result)
                    except (ValueError, ZeroDivisionError):
                        pass
    
    def _algebraic_simplification(self):
        """Aplica simplificaciones algebraicas."""
        for i, instr in enumerate(self.instructions):
            # Multiplicación por 1
            if instr.op == "*" and instr.arg2 == "1":
                self.instructions[i] = type(instr)("=", instr.arg1, None, instr.result)
            # Multiplicación por 0
            elif instr.op == "*" and instr.arg2 == "0":
                self.instructions[i] = type(instr)("=", "0", None, instr.result)
            # Suma de 0
            elif instr.op == "+" and instr.arg2 == "0":
                self.instructions[i] = type(instr)("=", instr.arg1, None, instr.result)
            # Resta de 0
            elif instr.op == "-" and instr.arg2 == "0":
                self.instructions[i] = type(instr)("=", instr.arg1, None, instr.result)
            # División por 1
            elif instr.op == "/" and instr.arg2 == "1":
                self.instructions[i] = type(instr)("=", instr.arg1, None, instr.result)
    
    def _copy_propagation(self):
        """Propaga copias de variables."""
        # Identificar asignaciones simples (x = y)
        for instr in self.instructions:
            if instr.op == "=" and instr.arg2 is None and not self._is_literal(instr.arg1):
                self.copy_map[instr.result] = instr.arg1
        
        # Propagar las copias
        for i, instr in enumerate(self.instructions):
            # No tocar etiquetas ni saltos
            if instr.op in ["LABEL", "GOTO"]:
                continue
            
            # Propagar en arg1
            if instr.arg1 in self.copy_map:
                self.instructions[i].arg1 = self.copy_map[instr.arg1]
            
            # Propagar en arg2
            if instr.arg2 in self.copy_map:
                self.instructions[i].arg2 = self.copy_map[instr.arg2]
            
            # No propagar en el resultado
    
    def _dead_code_elimination(self):
        """Elimina código muerto."""
        # Marcar instrucciones a eliminar
        to_remove = []
        for i, instr in enumerate(self.instructions):
            # No eliminar etiquetas, saltos, ni prints
            if instr.op in ["LABEL", "GOTO", "IF", "IFFALSE", "PRINT", "RETURN"]:
                continue
            
            # Eliminar asignaciones a variables no utilizadas
            if instr.result and instr.result not in self.used_vars and instr.result.startswith('t'):
                to_remove.append(i)
        
        # Eliminar instrucciones marcadas (en orden inverso para no afectar los índices)
        for i in sorted(to_remove, reverse=True):
            self.instructions.pop(i)
        
        # Reconstruir mapa de etiquetas
        self._build_label_map()
    
    def _jump_optimization(self):
        """Optimiza saltos."""
        # Eliminar saltos a la siguiente instrucción
        i = 0
        while i < len(self.instructions) - 1:
            instr = self.instructions[i]
            next_instr = self.instructions[i + 1]
            
            if instr.op == "GOTO" and next_instr.op == "LABEL" and instr.result == next_instr.result:
                # Eliminar el salto innecesario
                self.instructions.pop(i)
            else:
                i += 1
        
        # Reconstruir mapa de etiquetas
        self._build_label_map()
        
        # Optimizar cadenas de saltos
        changed = True
        while changed:
            changed = False
            for i, instr in enumerate(self.instructions):
                if instr.op == "GOTO":
                    target_label = instr.result
                    if target_label in self.label_map:
                        target_index = self.label_map[target_label]
                        if target_index < len(self.instructions) - 1:
                            next_instr = self.instructions[target_index + 1]
                            if next_instr.op == "GOTO":
                                # Reemplazar el salto actual por un salto directo al destino final
                                self.instructions[i].result = next_instr.result
                                changed = True

def generar_codigo_intermedio(ast=None):
    """
    Genera código intermedio a partir de un AST.
    
    Args:
        ast: Nodo raíz del árbol AST. Si es None, se construye a partir de los tokens.
        
    Returns:
        Generador TAC con el código intermedio generado.
    """
    if ast is None:
        tokens = leer_tokens()
        if not tokens:
            print("Error: No se encontraron tokens para analizar.")
            return None
        
        ast = construir_ast(tokens)
        if not ast:
            print("Error: No se pudo construir el árbol sintáctico.")
            return None
    
    # Generar código TAC
    generator = TACGenerator()
    generator.generate_code_from_ast(ast)
    return generator

def optimizar_codigo_intermedio(tac_generator):
    """
    Optimiza el código intermedio generado.
    
    Args:
        tac_generator: Generador TAC con instrucciones.
        
    Returns:
        Generador TAC con instrucciones optimizadas.
    """
    optimizer = TACOptimizer(tac_generator)
    tac_generator.instructions = optimizer.optimize()
    return tac_generator

def generar_grafico_tac(tac_generator, filename):
    """
    Genera un gráfico visual del código de tres direcciones utilizando Graphviz.
    
    Args:
        tac_generator: Generador TAC con instrucciones.
        filename: Nombre del archivo de salida (sin extensión).
        
    Returns:
        Ruta del archivo de imagen generado.
    """
    dot = graphviz.Digraph(comment='Three Address Code')
    dot.attr(rankdir='TB')
    
    # Crear nodos para cada instrucción
    for i, instr in enumerate(tac_generator.instructions):
        node_id = f"instr_{i}"
        label = str(instr)
        dot.node(node_id, label, shape='box', style='filled', fillcolor='lightblue')
        
        # Si es una instrucción de salto, conectarla con su destino
        if instr.op in ["GOTO", "IF", "IFFALSE"]:
            for j, target_instr in enumerate(tac_generator.instructions):
                if target_instr.op == "LABEL" and target_instr.result == instr.result:
                    dot.edge(node_id, f"instr_{j}", color='red')
    
    # Conectar instrucciones secuenciales
    for i in range(len(tac_generator.instructions) - 1):
        if tac_generator.instructions[i].op not in ["GOTO"]:
            dot.edge(f"instr_{i}", f"instr_{i+1}", style='dashed')
    
    # Renderizar el grafo a un archivo de imagen
    try:
        dot.render(filename, format='png', cleanup=True)
        return f"{filename}.png"
    except Exception as e:
        print(f"Error al generar el gráfico: {str(e)}")
        return None

def guardar_codigo_intermedio(tac_generator, filename="codigo_intermedio.tac"):
    """
    Guarda el código intermedio en un archivo.
    
    Args:
        tac_generator: Generador TAC con instrucciones.
        filename: Nombre del archivo de salida.
        
    Returns:
        True si se guardó correctamente, False en caso contrario.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(tac_generator.get_code_as_string())
        return True
    except Exception as e:
        print(f"Error al guardar el código intermedio: {str(e)}")
        return False