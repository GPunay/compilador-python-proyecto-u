import shutil
import subprocess
import os

enlace = "a"
tempAsm = [] # almacena las variables temporales y la etiqueta ensamblador con la que estan vinculadas [t0, eax]
vars_txt = [] #Son las variables de texto, para identificar el metodo de impresion

def asign_temp(temps, temp, val):
    new = []
    for t in temps:
        if temp == t[0]:
            t = [temp, val]
        new.append(t)
    return new

def var_txt(nombre, valor):
    global vars_txt
    if "\"" in valor or "\'" in valor:
        vars_txt.append(nombre)

#funcion para realizar las operaciones algebraicas que permite el sistema
def operaciones_asm(asm, signo, op1, op2):
    global enlace
    global tempAsm
    if op1[0]=='t' or op2[0]=='t':
        for t in tempAsm:        
            if t[0] in str(op1):
                op1 = t[1]
             
            if  t[0] in str(op2):
                op2 = t[1]              
             
        asm.append(f"    mov e{enlace}x, {op1}")
    else:
        if not op1.isdigit():
            op1 = f"[{op1}]"
        asm.append(f"    mov e{enlace}x, {op1.strip()}")
        if not op2.isdigit():
            op2 = f"[{op2}]"

    if signo=='+':
        asm.append(f"    add e{enlace}x, {op2.strip()}")
    elif signo=='-':
        asm.append(f"    sub e{enlace}x, {op2.strip()}")
    elif signo=='/':
        asm.append(f"    xor e{enlace}x, {op2.strip()}")
    elif signo=='*':
        asm.append(f"    imul e{enlace}x, {op2.strip()}")
    return asm

#funcion para operaciones logicas
def logica_asm(asm, signo, op1, op2, l):
    global enlace
    global tempAsm
    if op1[0]=='t' or op2[0]=='t':
        for t in tempAsm:        
            if t[0] in str(op1):
                op1 = t[1]
             
            if  t[0] in str(op2):
                op2 = t[1]              
             
        asm.append(f"    mov e{enlace}x, {op1}")
    else:
        if not op1.isdigit():
            op1 = f"[{op1}]"
        asm.append(f"    mov e{enlace}x, {op1.strip()}")
        if not op2.isdigit():
            op2 = f"[{op2}]"

    asm.append(f"    cmp e{enlace}x, {op2.strip()}")
    if signo=='<':
        asm.append(f"    jl L{l}")
    elif signo=='>':
        asm.append(f"    jg L{l}")
    elif signo=='<=':
        asm.append(f"    jle L{l}")
    elif signo=='>=':
        asm.append(f"    jge L{l}")
    else:
        asm.append(f"    je L{l}")
    return asm

def convertir_tac_a_asm(archivo):
    
    archivo_tac=archivo + ".tac"
    archivo_asm="ensamblador.asm"
    if(os.path.exists(archivo_tac)):
        tac = []
        with open(archivo_tac, "r", encoding="utf-8") as txt:
            print(f"\nArchivo ha sido leido correctamente\n")
            tac = txt.readlines()
        
        asm = [
            "BITS 32",
            "extern _ExitProcess@4",
            "extern _WriteConsoleA@20",
            "extern _GetStdHandle@4",
            "section .data"
        ]
        
        variables = {}#Almacena las variables para declararlas en .data
        vars = []#Almacena la variables declaradas para no repetir su declaracion
        vals = []#Almacena los valores de las variables
        temp = []#Almacen las variables temporales y a qur variable se asignan su valor
        global tempAsm
        global enlace
        etiquetas = []#Almacenara las etiqueta L0, L1,... para las condicionales y ciclos
        ctag = 0 #Cuenta el numero de etiquetas
        msg = 0 #contador para los mensajes impresos en pantalla
        global vars_txt

        # Primera pasada: Definir variables y etiquetas
        for linea in tac:
            linea = linea.strip()
            if linea and " = " in linea:
                nombre, valor = linea.split(" = ")
                #Se declaran las variables siempre y cuando no se repitan
                if not nombre in vars:
                    if nombre[0] == 't' and nombre[1].isdigit():
                        temp.append(nombre)

                    elif "\"" in valor or "\'" in valor:  #Si es una cadena de caracteres
                        asm.append(f"    {nombre} dd {valor}, 0Ah, 0")
                        var_txt(nombre, valor)
                    elif valor in vars_txt:
                        asm.append(f"   {nombre} resb 255")
                        vars_txt.append(nombre)
                    else:
                        if valor in vars or any(v in valor for v in ["+", "-", "*", "/"]) or (valor.isdigit() or valor[0]=="\""):
                            valor = "0"
                        elif  valor[0] == 't' and valor[1].isdigit():
                            #temp = asign_temp(temp, valor, nombre)
                            valor = "0"
                        variables[nombre.strip()] = valor.strip()
                        vars.append(nombre)   
                        vals.append(valor) 
                        asm.append(f"    {nombre} dd {valor}")
            elif linea.endswith(":"):
                etiquetas.append(linea.strip())
        
        #Filtra solo las temporales de asignacion
        new = []
        for t in temp:
            if len(t)>1:
                new.append(t)
        
        temp=new

    # Sección de código
        asm.append("    mensaje db 256 dup(0)  ; Reservar espacio para la cadena (máximo 256 caracteres)")
        asm.append("    resultado db \"0000\", 0")
        asm.append("    longitud db 10")
        asm.append("    longitud_mensaje db 0")
        asm.append("    escritos dd 0")
        asm.append("section .text")
        asm.append("global _main")
        asm.append("_main:")

        asm_block = [[]] #Es un arreglo que servira para guardar los bloques de datos que se usaran en las condicionales y ciclos
        flag=False
        flag2=False
        loop=False #Cambia el comportamiento de la etiqueta ifelse para que funcione como ciclo
        i=0
        #Cuenta el numero de temporales seguidas antes de asignar una variable

        # Segunda pasada: Generar código ASM
        for linea in tac:
            linea = linea.strip()

            # Asignaciones y operaciones aritméticas
            if " = " in linea:
                nombre, valor = linea.split(" = ")
                nombre, valor = nombre.strip(), valor.strip()

                
                #Cuando se asigna el valor de una variable o una constante
                if valor.isdigit() or valor in vars or valor in temp:
                    enlace = chr(ord(enlace) - 1)
                    if nombre in vars and valor in temp:#Cuando se asigna el valor directamente de una temporal                   
                        
                        asm_block[ctag].append(f"    mov [{nombre}], e{enlace}x")
                    else:

                        if valor.isdigit(): 
                            asm_block[ctag].append(f"    mov eax, {valor}")
                            asm_block[ctag].append(f"    mov [{nombre}], eax")
                        elif nombre in temp:
                            #no hace nada
                            print("")
                        else:
                            
                            asm_block[ctag].append(f"    mov eax, [{valor}]")
                            asm_block[ctag].append(f"    mov [{nombre}], eax")
                    enlace='a'
                elif "\"" in valor or "\'" in valor: #Si se esta asignando un valor
                    asm_block[ctag].append("; Asignar texto manualmente dentro de `_main`")
                    valor = valor.strip().replace("\"", "")
                    valor = valor.strip().replace("\'", "")
                    msg = 0
                    for v in valor:
                        asm_block[ctag].append(f"    mov byte [{nombre} + {msg}], '{v}'")
                        msg+=1
                    asm_block[ctag].append(f"    mov byte [{nombre} + {msg}], 0Ah  ; Salto de línea")
                    asm_block[ctag].append(f"    mov byte [{nombre} + {msg + 1}], 0    ; Terminador nulo")
                elif valor in vars_txt:
                    asm_block[ctag].append(f"    mov al, [{valor}]  ; Salto de línea")
                    asm_block[ctag].append(f"    mov [{nombre}], al  ; Salto de línea")
                    asm_block[ctag].append(f"    mov byte [{nombre} + {msg + 1}], 0    ; Terminador nulo")
                elif '<' in valor or '>' in valor or '<=' in valor or '>=' in valor or '==' in valor:#Operaciones logicas
                    if '<' in valor:
                        signo = '<'
                    elif '>' in valor:
                        signo = '>'
                    elif '<=' in valor:
                        signo = '<='
                    elif '>=' in valor:
                        signo = '>='
                    else:
                        signo = '=='
                    
                    op1, op2 = valor.split(" "+ signo + " ")
                    if loop:
                        asm_block[ctag]= logica_asm(asm_block[ctag], signo, op1, op2, ctag+1)
                    else:
                        asm_block[ctag]= logica_asm(asm_block[ctag], signo, op1, op2, ctag)
                else:#operacion Algebraica
                    #Identificar el tipo de operacion
                    signo = ''
                    
                    if '+' in valor:
                        signo = '+'

                    elif '-' in valor:
                        signo = '-'
                    elif '*' in valor:
                        signo = '*'
                    elif '/' in valor:
                        signo = '/'
                    
                    op1, op2 = valor.split(" "+ signo + " ")
                    asm_block[ctag]= operaciones_asm(asm_block[ctag], signo, op1, op2)

                    #Almacenar la direccion del resultado
                    tempAsm.append([nombre, f"e{enlace}x"])
                    enlace = chr(ord(enlace) + 1)

            # Condicionales ifFalse
            elif linea.startswith("ifFalse"):
                condicion, etiqueta = linea.replace("ifFalse ", "").split(" goto ")
                #Se crea un cuadro aparte donde se realiza las acciones en el caso de que se cumpla la condicion
                if not loop:
                    ctag+=1
                    asm_block.append([])
                    asm_block[ctag].append(f"L{ctag-1}:")
                


            # Saltos directos
            elif linea.startswith("goto "):
                etiqueta = linea.replace("goto L", "").strip()
                if loop:
                    ctag+=1
                    asm_block[ctag].append(f"jmp L{ctag-1}")
                    
                else:
                    ctag-=1
                flag=True
            #Ciclo
            elif linea.startswith("L"):
                etiqueta = linea.replace("L", "").strip()
                
                if not flag:#Detecto un ciclo
                    asm_block.append([])
                    asm_block[ctag].append(f"L{ctag}:")
                    loop = True

            # Impresión de texto
            elif linea.startswith("print "):
                mensaje = linea.replace("print ", "")
                #Establecer en handle
                asm_block[ctag].append("; GetStdHandle(STD_OUTPUT_HANDLE = -11)")
                asm_block[ctag].append("    push -11")
                asm_block[ctag].append("    call _GetStdHandle@4")
                asm_block[ctag].append("    mov ebx, eax")
                #Imprimir text
                if "\"" in mensaje or "\'" in mensaje:
                    mensaje = mensaje.strip().replace("\"", "")
                    mensaje = mensaje.strip().replace("\'", "")
                    asm_block[ctag].append("; Asignar texto manualmente dentro de `_main`")
                    msg = 0
                    for m in mensaje:
                        asm_block[ctag].append(f"    mov byte [mensaje + {msg}], '{m}'")
                        msg+=1
                    asm_block[ctag].append(f"    mov byte [mensaje + {msg}], 0Ah  ; Salto de línea")
                    asm_block[ctag].append(f"    mov byte [mensaje + {msg + 1}], 0    ; Terminador nulo")
                    asm_block[ctag].append(f"    mov esi, mensaje")
                    asm_block[ctag].append("    call calcular_longitud")
                    asm_block[ctag].append("    call imprimir_mensaje")
                elif mensaje in vars_txt:
                    asm_block[ctag].append(f"    mov esi, {mensaje}")
                    asm_block[ctag].append("    call calcular_longitud")
                    asm_block[ctag].append("    call imprimir_mensaje")
                else: #Imprimir vairables
                    #Convertir la variable en una cadena
                    asm_block[ctag].append("")
                    asm_block[ctag].append("; Convertir sum a cadena")
                    asm_block[ctag].append("    mov eax, \"\"")
                    asm_block[ctag].append("    mov [resultado], eax")
                    asm_block[ctag].append(f"    mov eax, {mensaje}")
                    asm_block[ctag].append("    mov edi, resultado")
                    asm_block[ctag].append("    call convertir_a_cadena")
                    #Establecer en handle

                    #Imprimir en consola el mensaje deseado
                    asm_block[ctag].append("")
                    asm_block[ctag].append("; Imprimir sum en pantalla")
                    asm_block[ctag].append("    call imprimir_resultado")
            if flag:
                long = len(etiquetas)-1
                if loop:
                    flag=False
                    flag2=False
                    loop=False
                elif flag2 and i==2:
                    asm_block.append([])
                    asm_block[ctag].append(f"    jmp L{ctag+1}")
                    ctag+=2
                    asm_block[ctag].append(f"L{ctag-1}:")
                    flag = False
                    flag2= False
                    i=0
                if linea in etiquetas:
                    i+=1
                    flag2=True
                    

            asm_block[ctag].append("\n")
            print(linea)

        # Salida del programa
        for block in asm_block:      
            for b in block:
                asm.append(b) 
        
        asm.append("    push 0")
        asm.append("    call _ExitProcess@4")
        asm.append("    ret")
        asm.append("\n")
        #Agregar funciones para imprimir

        asm.append("imprimir_resultado:")
        asm.append("    lea eax, [escritos]")
        asm.append("    push 0")
        asm.append("    push eax")
        asm.append("    movzx eax, byte [longitud]")
        asm.append("    push eax")
        asm.append("    push resultado")
        asm.append("    push ebx")
        asm.append("    call _WriteConsoleA@20")
        asm.append("    ret")
        asm.append("\n")

        #funcion de convertir cadena
        asm.append("convertir_a_cadena:")
        asm.append("    push edx")
        asm.append("    push ebx")
        asm.append("    push eax")

        asm.append("    mov ebx, eax         ; Guardar la dirección de la variable")
        asm.append("    mov eax, [ebx]       ; Cargar el valor numérico")
        asm.append("    mov ecx, 10          ; Base decimal")
        asm.append("    mov edi, resultado + 4  ; Apuntar al final del buffer")

        asm.append("    ; Comprobar si el número es negativo")
        asm.append("    test eax, eax")
        asm.append("    jns .convertir  ; Si es positivo, continuar")

        asm.append("    ; Si es negativo, agregar '-' al inicio del buffer")
        asm.append("    neg eax")
        asm.append("    mov byte [resultado], '-'   ; Insertar '-'")
        asm.append("    mov edi, resultado + 4      ; Ajustar `EDI` correctamente")

        asm.append(".convertir:")
        asm.append(".loop:")
        asm.append("    mov edx, 0")
        asm.append("    div ecx              ; Divide EAX por 10  EDX contiene el residuo")
        asm.append("    add dl, '0'          ; Convertir dígito a ASCII")
        asm.append("    mov [edi], dl        ; Almacenar en el buffer")
        asm.append("    dec edi")
        asm.append("    cmp eax, 0")
        asm.append("    jne .loop            ; Si aún quedan dígitos, repetir")

        asm.append("    ; Mover `EDI` al inicio de la cadena antes de imprimir")
        asm.append("    mov edi, resultado")

        asm.append("    pop eax")
        asm.append("    pop ebx")
        asm.append("    pop edx")
        asm.append("    ret")
        asm.append("\n")

        #Funcion para imprimir texto
        asm.append("; Función para calcular la longitud del mensaje dinámico")
        asm.append("calcular_longitud:")
        asm.append("    mov ecx, 0  ; Inicializar contador de longitud")
        asm.append(".buscar_fin:")
        asm.append("    cmp byte [esi+ecx], 0")
        asm.append("    je .fin")
        asm.append("    inc ecx")
        asm.append("    jmp .buscar_fin")
        asm.append(".fin:")
        asm.append("    mov [longitud_mensaje], ecx  ; Almacenar longitud calculada")
        asm.append("    ret")

        asm.append("")
        asm.append("; Función para imprimir el mensaje actual")
        asm.append("imprimir_mensaje:")
        asm.append("    push 0")
        asm.append("    push escritos")
        asm.append("    push dword [longitud_mensaje]")
        asm.append("    push esi  ; Imprimir la cadena almacenada dinámicamente")
        asm.append("    push ebx")
        asm.append("    call _WriteConsoleA@20")
        asm.append("    ret")


        # Mostrar la cadena en pantalla con los saltos de línea correctos
        #print("\n".join(asm))

        # Escribir el archivo ensamblador
        with open(archivo_asm, 'w') as f:
            f.write("\n".join(asm))

        print(f"¡Conversión completa! Se ha generado {archivo_asm}")
        archi_asm = "\n".join(asm)
        #compilar(archivo)
        return archi_asm
    else:
        error = f"ERROR: ¡No se encontro el archivo {archivo_asm}"
        print(error)
        return error

def compilar(nombre, dir):
    # Verifica si NASM está en el sistema
    
    ruta = dir + "\\" + nombre
    if shutil.which("nasm") is None:
        print("Error: NASM no está instalado o no está en el PATH.")
    else:
        subprocess.run(["nasm", "-fwin32", "ensamblador.asm", "-o", f"{ruta}.obj"], shell=True)
        print("\nSe ha creado el .obj")
        if shutil.which("gcc") is None:
            print("Error: GCC no está instalado o no está en el PATH.")
        else:       
            # Enlazar con GCC
            subprocess.run(["gcc", f"{ruta}.obj", "-o", f"{ruta}.exe"], shell=True)
            print("\nSe ha creado el .exe")



