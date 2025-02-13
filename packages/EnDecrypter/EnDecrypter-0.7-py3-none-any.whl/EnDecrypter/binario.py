def texto_a_binario(texto):
    return ' '.join(format(ord(c), '08b') for c in texto)

def binario_a_texto(binario):
    binario_lista = binario.split(' ')
    texto = ''.join(chr(int(b, 2)) for b in binario_lista)
    return texto