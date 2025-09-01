#!/usr/bin/env python3
import sys
from scapy.all import rdpcap, ICMP, Raw
from colorama import Fore, Style

def cesar_descifrar(texto, corrimiento):
    """Aplica un corrimiento de César a la inversa (descifrar)."""
    resultado = []
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            nuevo = (ord(char) - base - corrimiento) % 26 + base
            resultado.append(chr(nuevo))
        else:
            resultado.append(char)
    return "".join(resultado)

def puntuacion_texto(texto):
    """Evalúa cuán probable es que el texto sea español simple."""
    score = 0
    comunes = [" el ", " la ", " que ", " de ", " los ", " un ", " en ", " y "]
    score += texto.count(" ")
    score += sum(texto.lower().count(pal) for pal in comunes)
    return score

def reconstruir_mensaje(pcap_file):
    paquetes = rdpcap(pcap_file)
    mensajes = {}

    for pkt in paquetes:
        if pkt.haslayer(ICMP) and pkt.haslayer(Raw):
            raw_data = pkt[Raw].load
            if len(raw_data) == 48:  # tu estructura
                icmp_id = pkt[ICMP].id
                seq = pkt[ICMP].seq
                char = raw_data[-1:].decode(errors="ignore")

                if icmp_id not in mensajes:
                    mensajes[icmp_id] = {}
                mensajes[icmp_id][seq] = char

    if not mensajes:
        print("No se encontraron paquetes ICMP válidos en la captura.")
        sys.exit(1)

    primer_id = next(iter(mensajes))
    reconstruido = "".join(mensajes[primer_id][i] for i in sorted(mensajes[primer_id]))
    return reconstruido

def main():
    if len(sys.argv) != 2:
        print(f"Uso: sudo python {sys.argv[0]} <archivo.pcapng>")
        sys.exit(1)

    archivo = sys.argv[1]
    mensaje_cifrado = reconstruir_mensaje(archivo)

    print(f"\nMensaje capturado (cifrado): {mensaje_cifrado}\n")

    mejores = []
    for corrimiento in range(26):
        descifrado = cesar_descifrar(mensaje_cifrado, corrimiento)
        score = puntuacion_texto(descifrado)
        mejores.append((score, corrimiento, descifrado))

    mejores.sort(reverse=True, key=lambda x: x[0])
    mejor = mejores[0]

    print("Posibles descifrados:\n")
    for score, corrimiento, descifrado in mejores:
        if corrimiento == mejor[1]:
            print(Fore.GREEN + f"{corrimiento:<2}   {descifrado}" + Style.RESET_ALL)
        else:
            print(f"{corrimiento:<2}   {descifrado}")

if __name__ == "__main__":
    main()
# Comando para uso: sudo python readv2.py cesar.pcapng 