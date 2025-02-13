def encriptar_cifrado_cesar(texto, desplazamiento):
    resultado = []

    for char in texto:
        if char.isalpha():
            # Determinamos si la letra es mayuscula o minuscula
            base = ord('A') if char.isupper() else ord('a')
            # Calculamos el desplazamiento en el alfabeto
            desplazado = (ord(char) - base + desplazamiento) % 26 + base
            resultado.append(chr(desplazado))
        else:
            # Si no es una letra (por ejemplo, espacio o puntuacion), la dejamos igual
            resultado.append(char)
    
    return ''.join(resultado)

def desencriptar_cifrado_cesar(texto, desplazamiento):
    resultado = []

    for char in texto:
        if char.isalpha():
            # Determinamos si la letra es mayuscula o minuscula
            base = ord('A') if char.isupper() else ord('a')
            # Calculamos el desplazamiento en el alfabeto
            desplazado = (ord(char) - base - desplazamiento) % 26 + base
            resultado.append(chr(desplazado))
        else:
            # Si no es una letra (por ejemplo, espacio o puntuacion), la dejamos igual
            resultado.append(char)
    
    return ''.join(resultado)