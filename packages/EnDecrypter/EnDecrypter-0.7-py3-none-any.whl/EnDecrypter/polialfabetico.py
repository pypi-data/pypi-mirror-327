import string

def generar_alfabeto():
    """Genera el alfabeto en mayusculas"""
    return string.ascii_uppercase

def limpiar_texto(texto):
    """Elimina caracteres que no son letras y convierte el texto a mayúsculas"""
    return ''.join([c for c in texto.upper() if c in string.ascii_uppercase])

def cifrar_polialfabetico(texto, clave):
    """Cifra el texto utilizando el cifrado de Vigenere con la clave proporcionada"""
    alfabeto = generar_alfabeto()
    texto_limpio = limpiar_texto(texto)
    clave = limpiar_texto(clave)

    texto_cifrado = []
    i = 0 # Indice para recorrer la clave

    for letra in texto_limpio:
        if letra in alfabeto:
            # Desplazamiento segun la letra de la clave
            desplazamiento = alfabeto.index(clave[i % len(clave)]) # Repite la clave si es mas corta que el texto
            nueva_letra = alfabeto[(alfabeto.index(letra) + desplazamiento) % 26]
            texto_cifrado.append(nueva_letra)
            i += 1
        else:
            # Si el caracterer no es una letra, lo dejamos sin cifrar
            texto_cifrado.append(letra)
    
    return ''.join(texto_cifrado)

def descifrar_polialfabetico(texto, clave):
    """Descifra el texto utilizando el cifrado de Vigenere con la clave proporcionada"""
    alfabeto = generar_alfabeto()
    texto_limpio = limpiar_texto(texto)
    clave = limpiar_texto(clave)

    texto_descifrado = []
    i = 0 # Indice para recorrer la clave

    for letra in texto_limpio:
        if letra in alfabeto:
            # Desplazamiento inverso segun la letra de la clave
            desplazamiento = alfabeto.index(clave[i % len(clave)])
            nueva_letra = alfabeto[(alfabeto.index(letra) - desplazamiento) % 26]
            texto_descifrado.append(nueva_letra)
            i += 1
        else:
            # Si el caracterer no es una letra, lo dejamos sin descifrar
            texto_descifrado.append(letra)
    
    return ''.join(texto_descifrado)

