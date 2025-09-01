#!/usr/bin/env python3
import sys

def cifrado_cesar(texto, corrimiento):
    resultado = ""
    for char in texto:
        if char.isalpha():  # Solo ciframos letras
            # Determinamos si es mayúscula o minúscula
            base = ord('A') if char.isupper() else ord('a')
            # Aplicamos el corrimiento usando módulo 26
            resultado += chr((ord(char) - base + corrimiento) % 26 + base)
        else:
            # Mantenemos el carácter sin cambios (espacios, puntuación)
            resultado += char
    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python cesar.py \"mensaje\" corrimiento")
        sys.exit(1)
    
    mensaje = sys.argv[1]
    corrimiento = int(sys.argv[2])

    cifrado = cifrado_cesar(mensaje, corrimiento)
    print(cifrado)
# Comando para uso: python cesar.py "criptografia y seguridad en redes" 9