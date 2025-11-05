from Crypto.Cipher import AES, DES, DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def normalizar_clave(clave_entrada: bytes, algoritmo: str) -> bytes:
    if algoritmo == "AES":
        # AES-256 requiere 32 bytes
        tam = 32
        if len(clave_entrada) < tam:
            clave_entrada += get_random_bytes(tam - len(clave_entrada))
        else:
            clave_entrada = clave_entrada[:tam]
        return clave_entrada

    elif algoritmo == "DES":
        # DES usa 8 bytes
        tam = 8
        if len(clave_entrada) < tam:
            clave_entrada += get_random_bytes(tam - len(clave_entrada))
        else:
            clave_entrada = clave_entrada[:tam]
        return clave_entrada

    elif algoritmo == "3DES":
        # 3DES requiere 24 bytes (K1, K2, K3)
        tam = 24
        if len(clave_entrada) < tam:
            clave_entrada += get_random_bytes(tam - len(clave_entrada))
        else:
            clave_entrada = clave_entrada[:tam]

        # Evitar degeneración a DES (K1==K2 o K2==K3 o K1==K3)
        K1 = clave_entrada[:8]
        K2 = clave_entrada[8:16]
        K3 = clave_entrada[16:]

        if K1 == K2 or K2 == K3 or K1 == K3:
            K2 = get_random_bytes(8)
            K3 = get_random_bytes(8)
            clave_entrada = K1 + K2 + K3

        return clave_entrada


def normalizar_iv(iv_entrada: bytes, algoritmo: str) -> bytes:
    if algoritmo == "AES":
        return iv_entrada[:16]
    else:
        return iv_entrada[:8]


def cifrar_descifrar(texto_bytes, clave_final, iv_final, algoritmo):
    if algoritmo == "AES":
        motor = AES.new(clave_final, AES.MODE_CBC, iv_final)
    elif algoritmo == "DES":
        motor = DES.new(clave_final, DES.MODE_CBC, iv_final)
    else:
        motor = DES3.new(clave_final, DES3.MODE_CBC, iv_final)

    cifrado = motor.encrypt(pad(texto_bytes, motor.block_size))

    # Descifrado
    if algoritmo == "AES":
        motor2 = AES.new(clave_final, AES.MODE_CBC, iv_final)
    elif algoritmo == "DES":
        motor2 = DES.new(clave_final, DES.MODE_CBC, iv_final)
    else:
        motor2 = DES3.new(clave_final, DES3.MODE_CBC, iv_final)

    descifrado = unpad(motor2.decrypt(cifrado), motor2.block_size)

    return cifrado, descifrado


def a_hex(b):
    return b.hex()


def a_b64(b):
    return base64.b64encode(b).decode()


# ------------------ PROGRAMA PRINCIPAL ------------------

mensaje = input("Texto a cifrar:\n> ")
llave = input("\nLlave (puedes ingresar en HEX o texto):\n> ")
iv = input("\nVector de inicialización (IV) (HEX o texto):\n> ")

# Intentar interpretar como hex, si no, usar como texto
try:
    llave_bytes = bytes.fromhex(llave)
except:
    llave_bytes = llave.encode()

try:
    iv_bytes = bytes.fromhex(iv)
except:
    iv_bytes = iv.encode()

mensaje_bytes = mensaje.encode()

print("\n--- RESULTADOS ---\n")

for alg in ["AES", "DES", "3DES"]:
    clave_final = normalizar_clave(llave_bytes, alg)
    iv_final = normalizar_iv(iv_bytes, alg)

    cifrado, descifrado = cifrar_descifrar(mensaje_bytes, clave_final, iv_final, alg)

    print(f"Llave final {alg}: {clave_final.hex()}")
    print(f"IV final {alg}: {iv_final.hex()}\n")
    print(f"{alg} (Cifrado hex): {a_hex(cifrado)}")
    print(f"{alg} (Cifrado base64): {a_b64(cifrado)}")
    print(f"{alg} (Descifrado): {descifrado.decode()}\n")
