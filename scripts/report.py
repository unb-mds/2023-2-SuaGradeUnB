import subprocess
import signal

command = "python3 -m http.server --cgi 8080 -d ./api/htmlcov".split()
server_process = subprocess.Popen(command)

try:
    print("\nCtrl + C pressed. Stopping the server.\n")
    server_process.wait()
except KeyboardInterrupt:
    subprocess.run(['make', 'cleanup'])
    server_process.send_signal(signal.SIGINT)
    server_process.wait()

server_process.terminate()
