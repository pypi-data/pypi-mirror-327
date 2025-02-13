def cifrar_transposicion(texto, num_rails):
    """Cifra el texto utilizando el Cifrado de Rail Fence"""
    if num_rails < 2:
        return texto
        
    # Crear una tabla vacía con el número de renglones especificado
    rails = [[] for _ in range(num_rails)]
    
    direccion_abajo = False
    rail = 0
    
    # Colocar las letras en las posiciones de la tabla
    for char in texto:
        rails[rail].append(char)
        if rail == 0 or rail == num_rails - 1:
            direccion_abajo = not direccion_abajo
        rail += 1 if direccion_abajo else -1
    
    # Unir las filas de la tabla en una cadena para obtener el texto cifrado
    return ''.join([''.join(rail) for rail in rails])

def descifrar_transposicion(texto, num_rails):
    """Descifra el texto cifrado utilizando el Cifrado de Rail Fence"""
    if num_rails < 2:
        return texto
    
    if not texto:
        return ""
        
    # Primero, calculamos las posiciones donde irían los caracteres
    posiciones = []
    rail = 0
    direccion_abajo = False
    
    # Creamos una lista de posiciones en el orden en que se llenaron
    for i in range(len(texto)):
        posiciones.append(rail)
        if rail == 0 or rail == num_rails - 1:
            direccion_abajo = not direccion_abajo
        rail += 1 if direccion_abajo else -1
    
    # Creamos un diccionario para mapear las posiciones a sus índices en el texto cifrado
    rails_indices = {}
    for i in range(num_rails):
        rails_indices[i] = []
    
    # Guardamos los índices donde aparece cada rail
    for i, pos in enumerate(posiciones):
        rails_indices[pos].append(i)
    
    # Reconstruimos el texto original
    actual_pos = 0
    resultado = [''] * len(texto)
    
    # Para cada rail, tomamos los caracteres del texto cifrado y los colocamos
    # en sus posiciones originales
    for rail in range(num_rails):
        for pos in rails_indices[rail]:
            if actual_pos < len(texto):
                resultado[pos] = texto[actual_pos]
                actual_pos += 1
    
    return ''.join(resultado)