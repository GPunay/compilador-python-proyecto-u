BITS 32
extern _ExitProcess@4
extern _WriteConsoleA@20
extern _GetStdHandle@4
section .data
    x dd 0
    y dd 0
    sum dd 0
    resta dd 0
    divi dd 0
    mult dd 0
    h dd 'h', 0Ah, 0
    mensaje db 256 dup(0)  ; Reservar espacio para la cadena (máximo 256 caracteres)
    resultado db "0000", 0
    longitud db 10
    longitud_mensaje db 0
    escritos dd 0
section .text
global _main
_main:
    mov eax, 12
    mov [x], eax


    mov eax, 30
    mov [y], eax


    mov eax, [x]
    add eax, [y]


    mov [sum], eax


    mov eax, [x]
    sub eax, [y]


    mov [resta], eax


    mov eax, [y]
    xor eax, [x]


    mov [divi], eax


    mov eax, [x]
    imul eax, [y]


    mov [mult], eax


    mov eax, 500
    mov [y], eax


    mov eax, [sum]
    cmp eax, [y]
    jg L0








; GetStdHandle(STD_OUTPUT_HANDLE = -11)
    push -11
    call _GetStdHandle@4
    mov ebx, eax
; Asignar texto manualmente dentro de `_main`
    mov byte [mensaje + 0], 'N'
    mov byte [mensaje + 1], 'o'
    mov byte [mensaje + 2], ' '
    mov byte [mensaje + 3], 'h'
    mov byte [mensaje + 4], 'e'
    mov byte [mensaje + 5], 'm'
    mov byte [mensaje + 6], 'o'
    mov byte [mensaje + 7], 's'
    mov byte [mensaje + 8], ' '
    mov byte [mensaje + 9], 'd'
    mov byte [mensaje + 10], 'e'
    mov byte [mensaje + 11], 's'
    mov byte [mensaje + 12], 'p'
    mov byte [mensaje + 13], 'e'
    mov byte [mensaje + 14], 'g'
    mov byte [mensaje + 15], 'a'
    mov byte [mensaje + 16], 'd'
    mov byte [mensaje + 17], 'o'
    mov byte [mensaje + 18], 0Ah  ; Salto de línea
    mov byte [mensaje + 19], 0    ; Terminador nulo
    mov esi, mensaje
    call calcular_longitud
    call imprimir_mensaje
    jmp L1
L0:


; GetStdHandle(STD_OUTPUT_HANDLE = -11)
    push -11
    call _GetStdHandle@4
    mov ebx, eax
; Asignar texto manualmente dentro de `_main`
    mov byte [mensaje + 0], 'H'
    mov byte [mensaje + 1], 'o'
    mov byte [mensaje + 2], 'l'
    mov byte [mensaje + 3], 'a'
    mov byte [mensaje + 4], ' '
    mov byte [mensaje + 5], 'm'
    mov byte [mensaje + 6], 'u'
    mov byte [mensaje + 7], 'n'
    mov byte [mensaje + 8], 'd'
    mov byte [mensaje + 9], 'o'
    mov byte [mensaje + 10], 0Ah  ; Salto de línea
    mov byte [mensaje + 11], 0    ; Terminador nulo
    mov esi, mensaje
    call calcular_longitud
    call imprimir_mensaje


L1:


    mov eax, 10
    mov [x], eax


    mov eax, 0
    mov [y], eax


    mov eax, 0
    mov [sum], eax


L2:


    mov eax, [sum]
    cmp eax, 2
    jg L3




; GetStdHandle(STD_OUTPUT_HANDLE = -11)
    push -11
    call _GetStdHandle@4
    mov ebx, eax
; Asignar texto manualmente dentro de `_main`
    mov byte [mensaje + 0], 's'
    mov byte [mensaje + 1], 'i'
    mov byte [mensaje + 2], 0Ah  ; Salto de línea
    mov byte [mensaje + 3], 0    ; Terminador nulo
    mov esi, mensaje
    call calcular_longitud
    call imprimir_mensaje


    mov eax, [sum]
    add eax, 1


    mov [sum], eax


jmp L2


L3:


; Asignar texto manualmente dentro de `_main`
    mov byte [h + 0], 'h'
    mov byte [h + 1], 0Ah  ; Salto de línea
    mov byte [h + 2], 0    ; Terminador nulo


    push 0
    call _ExitProcess@4
    ret


imprimir_resultado:
    lea eax, [escritos]
    push 0
    push eax
    movzx eax, byte [longitud]
    push eax
    push resultado
    push ebx
    call _WriteConsoleA@20
    ret


convertir_a_cadena:
    push edx
    push ebx
    push eax
    mov ebx, eax         ; Guardar la dirección de la variable
    mov eax, [ebx]       ; Cargar el valor numérico
    mov ecx, 10          ; Base decimal
    mov edi, resultado + 4  ; Apuntar al final del buffer
    ; Comprobar si el número es negativo
    test eax, eax
    jns .convertir  ; Si es positivo, continuar
    ; Si es negativo, agregar '-' al inicio del buffer
    neg eax
    mov byte [resultado], '-'   ; Insertar '-'
    mov edi, resultado + 4      ; Ajustar `EDI` correctamente
.convertir:
.loop:
    mov edx, 0
    div ecx              ; Divide EAX por 10  EDX contiene el residuo
    add dl, '0'          ; Convertir dígito a ASCII
    mov [edi], dl        ; Almacenar en el buffer
    dec edi
    cmp eax, 0
    jne .loop            ; Si aún quedan dígitos, repetir
    ; Mover `EDI` al inicio de la cadena antes de imprimir
    mov edi, resultado
    pop eax
    pop ebx
    pop edx
    ret


; Función para calcular la longitud del mensaje dinámico
calcular_longitud:
    mov ecx, 0  ; Inicializar contador de longitud
.buscar_fin:
    cmp byte [esi+ecx], 0
    je .fin
    inc ecx
    jmp .buscar_fin
.fin:
    mov [longitud_mensaje], ecx  ; Almacenar longitud calculada
    ret

; Función para imprimir el mensaje actual
imprimir_mensaje:
    push 0
    push escritos
    push dword [longitud_mensaje]
    push esi  ; Imprimir la cadena almacenada dinámicamente
    push ebx
    call _WriteConsoleA@20
    ret