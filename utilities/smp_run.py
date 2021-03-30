from pyngrok import ngrok
import subprocess
import time

server_running = False
run_bat_path = "D:/Joel/rileys-server/server/TEKY_RUN.bat"
server_path = "D:/Joel/rileys-server/server"
server_ip = None

def startServer(bat_path=run_bat_path, result=None):
    global server_running
    global server_ip
    if server_running:
        return False
    server_running = True
    mc_server = ngrok.connect(25565, "tcp")
    server_ip = mc_server.public_url
    if result != None:
        result.result = mc_server.public_url
    p = subprocess.check_output(bat_path, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=server_path)
    print("starting server: " + mc_server.public_url)
    print(p)
    return mc_server.public_url

if __name__ == "__main__":
    startServer("D:/Joel/rileys-server/server/TEKY_RUN.bat")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
