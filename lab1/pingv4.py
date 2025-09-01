#!/usr/bin/env python3
import sys
from scapy.all import IP, ICMP, send
import time
import random

# Payload base de 48 bytes (primeros 47 bytes imitan ping real)
payload_base = bytes([
    0x62, 0x60, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16,
    0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e,
    0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26,
    0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e,
    0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35
])  # 47 bytes

def enviar_cesar_icmp(destino, mensaje):
    icmp_id = random.randint(0, 0xFFFF)
    seq_num = 0

    for char in mensaje:
        # Convertimos el carácter a byte y lo colocamos en la última posición
        payload = payload_base + char.encode()  # 48 bytes totales

        # Creamos el paquete ICMP
        paquete = IP(dst=destino, ttl=64)/ICMP(id=icmp_id, seq=seq_num)/payload

        # Enviamos el paquete
        send(paquete, verbose=False)
        print(f"Enviado: '{char}' (ID={icmp_id}, SEQ={seq_num})")

        seq_num += 1
        time.sleep(0.1)  # Delay para simular ping normal

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python pingv4.py <IP_destino> \"mensaje_cifrado\"")
        sys.exit(1)

    destino = sys.argv[1]
    mensaje_cifrado = sys.argv[2]
    enviar_cesar_icmp(destino, mensaje_cifrado)
    # Comando para uso: sudo python pingv4.py google.com "larycxpajorj h bnpdarmjm nw anmnb"