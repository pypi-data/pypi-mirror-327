# EnDecrypter

EnDecrypter es una librería de Python para cifrar y descifrar textos utilizando diferentes algoritmos de cifrado, incluyendo:

- Cifrado César
- Cifrado Monoalfabético
- Cifrado Binario
- Cifrado Polialfabetico
- Cifrado Transposicion

## Instalación

Para instalar la librería, ejecuta:

```bash
pip install EnDecrypter
```


## Documentacion

### Cifrados explicados

1. **Cifrado Cesar**:

El **Cifrado César** es uno de los métodos de cifrado más antiguos y simples. Consiste en desplazar cada letra del texto original por un número fijo de posiciones en el alfabeto. Por ejemplo, si usamos un desplazamiento de 3, la letra 'A' se convertiría en 'D', 'B' en 'E', y así sucesivamente. Este cifrado es fácilmente reversible usando el mismo desplazamiento.

**Metodos**

* `encriptar_cesar(texto, desplazamiento)`

Encripta el texto que desee y en el segundo parametro la cantidad de letras que se desplazara siguiendo el abecedario para adelante

* `desencriptar_cesar(texto, desplazamiento)`
  
Desencripta el texto que desee y en el segundo parametro la cantidad de letras que se desplazara siguiendo el abecedario para atras

2. **Binario**:

El **Cifrado Binario** convierte cada carácter del texto a su representación en binario. Cada letra del texto es reemplazada por su valor binario correspondiente en la codificación ASCII. Este cifrado es muy directo y no implica sustituciones o desplazamientos, pero se presenta en un formato completamente diferente (binario).

**Metodos**

* `texto_a_binario(texto)`

Convierte el texto a binario

* `binario_a_texto(binario)`

Convierte el binario a texto

3. **MonoAlfabetico**:

El **Cifrado Monoalfabético** es una forma de sustitución en la que cada letra del texto original se reemplaza por una letra diferente en el alfabeto, de acuerdo con un alfabeto de sustitución fijo. A diferencia del Cifrado César, en el que el desplazamiento es fijo, en el cifrado monoalfabético se puede usar cualquier tipo de mapeo aleatorio.

* `generar_alfabeto_sustitucion()`

Genera un alfabeto de sustitucion, es **Obligatoria** en el codigo cuando uses monoalfabetico

* `cifrar_monoalfabetico(texto, alfabeto_sustituto)`

Cifra el texto reemplazando cada letra con su correspondiente en el alfabeto de sustitución, manteniendo las mayúsculas y otros caracteres intactos.

* `descifrar_monoalfabetico(texto, alfabeto_sustituto)`

Descifra el texto utilizando el alfabeto de sustitución inverso para restaurar las letras originales, manteniendo las mayúsculas y otros caracteres intactos.

4. **Cifrado Polialfabetico**:

   
El **Cifrado polialfabético** es una mejora del monoalfabético, y uno de los más conocidos es el Cifrado de Vigenère. En este cifrado, en lugar de sustituir cada letra con una única letra según un alfabeto de sustitución fijo, se utilizan múltiples alfabetos de sustitución (de forma cíclica), lo que hace mucho más difícil romper el cifrado mediante análisis de frecuencia.

* `generar_alfabeto()`

Crea el alfabeto en mayúsculas de A-Z, utilizado para las operaciones de cifrado y descifrado.

* `limpiar_texto(texto)`

  Elimina cualquier carácter no alfabético (como espacios, puntuación, números, etc.) y convierte el texto a mayúsculas para estandarizar la entrada.

* `cifrar_polialfabetico(texto, clave)`

Cifra el texto utilizando el Cifrado de Vigenère.
Toma la clave y la repite cíclicamente para aplicar el desplazamiento según la letra correspondiente de la clave.

* `descifrar_polialfabetico(texto, clave)`

Descifra el texto cifrado utilizando el Cifrado de Vigenère.
Aplica el desplazamiento inverso usando la misma clave para devolver el texto a su forma original.

5. **Transposicion**:

El **Cifrado de Transposición** es un tipo de cifrado en el que se reorganizan las letras del texto original en lugar de sustituirlas por otras letras. Es decir, el texto original no se cambia, pero el orden de los caracteres se altera de acuerdo con una regla o patrón específico.

* `cifrar_transposicion(texto, num_rails)`

Cifra el texto usando el **Cifrado de Rail Fence**

* `descifrar_transposicion(texto, num_rails)`

Descifra el texto usando el **Cifrado de Rail Fence**

### Ejemplo de uso:

**Cifrado Cesar**
```python
from EnDecrypter.cesar import encriptar_cesar, desencriptar_cesar

texto = "Hola Mundo"
desplazamiento = 3

texto_encriptado = encriptar_cesar(texto, desplazamiento)
texto_desencriptado = desencriptar_cesar(texto, desplazamiento)

print(f"Texto encriptado: {texto_encriptado}")

print(f"Texto desencriptado: {texto_desencriptado}")
```

**Binario**
```python
from EnDecrypter.binario import binario_a_texto, texto_a_binario

texto = "Hola"

# El codigo binario debe estar en formato string
binario = '01001000 01101111 01101100 01100001'

textobinario = texto_a_binario(texto)
binariotexto = binario_a_texto(binario)

print(f"Texto a binario: {textobinario}")

print(f"Binario a texto: {binariotexto}")
```

**MonoAlfabetico**
```python
# La funcion para generar el alfabeto es obligatoria en el codigo
from EnDecrypter.monoalfabetico import generar_alfabeto_sustitucion, cifrar_monoalfabetico, descifrar_monoalfabetico

alfabeto_sustituto = generar_alfabeto_sustitucion()
texto_original = "Hola Mundo"

texto_cifrado = cifrar_monoalfabetico(texto_original, alfabeto_sustituto)
texto_descifrado = descifrar_monoalfabetico(texto_cifrado, alfabeto_sustituto)

print(f"{texto_original}")
print(f"{texto_cifrado}")
print(f"{texto_descifrado}")
```

**PoliAlfabetico**
```python
from EnDecrypter.polialfabetico import cifrar_polialfabetico, descifrar_polialfabetico


texto = "Hola Mundo"
clave = "clave"

texto_cifrado = cifrar_polialfabetico(texto, clave)
texto_descifrado = descifrar_polialfabetico(texto_cifrado, clave)

print(f"Texto original: {texto}")
print(f"Texto cifrado: {texto_cifrado}")
print(f"Texto descifrado: {texto_descifrado}")
```

**Transposicion**
```python
from EnDecrypter.transposicion import cifrar_transposicion, descifrar_transposicion

texto = "hello world"
num_rails = 3

texto_cifrado = cifrar_transposicion(texto, num_rails)
texto_descifrado = descifrar_transposicion(texto_cifrado, num_rails)


print(f"Texto original: {texto}")
print(f"Texto cifrado: {texto_cifrado}")
print(f"Texto descifrado: {texto_descifrado}")
```
