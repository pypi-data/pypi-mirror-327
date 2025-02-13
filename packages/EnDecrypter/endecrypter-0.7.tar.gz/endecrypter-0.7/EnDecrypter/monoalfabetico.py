import random
import string

def generar_alfabeto_sustitucion():
    alfabeto = list(string.ascii_lowercase)
    alfabeto_sustituto = alfabeto[:]
    random.shuffle(alfabeto_sustituto)
    return dict(zip(alfabeto, alfabeto_sustituto))

def cifrar_monoalfabetico(texto, alfabeto_sustituto):
        texto_cifrado = []
        for letra in texto:
            if letra.lower() in alfabeto_sustituto:
                nueva_letra = alfabeto_sustituto[letra.lower()]
                if letra.isupper():
                    nueva_letra = nueva_letra.upper()
                texto_cifrado.append(nueva_letra)
            else:
                texto_cifrado.append(letra)
        return ''.join(texto_cifrado)

def descifrar_monoalfabetico(texto, alfabeto_sustituto):
    alfabeto_inverso = {v: k for k, v in alfabeto_sustituto.items()}
    texto_descifrado = []
    for letra in texto:
        if letra.lower() in alfabeto_inverso:
            nueva_letra = alfabeto_inverso[letra.lower()]
            if letra.isupper():
                nueva_letra = nueva_letra.upper()
            texto_descifrado.append(nueva_letra)
        else:
            texto_descifrado.append(letra)
    return ''.join(texto_descifrado)