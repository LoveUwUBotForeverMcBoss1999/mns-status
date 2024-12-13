from flask import Flask, render_template, jsonify
import socket
import json
from mcstatus import JavaServer

app = Flask(__name__)

PROXY_SERVER = "panel2.mcboss.top"
PROXY_PORT = 25565

SERVERS = {
    "SkyBlock": {"ip": "panel2.mcboss.top", "port": 25570},
    "LifeSteal": {"ip": "panel2.mcboss.top", "port": 25566},
    "Hub": {"ip": "panel2.mcboss.top", "port": 25567},
    "Proxy": {"ip": "panel2.mcboss.top", "port": 25565},
    "SkyWars": {"ip": "panel2.mcboss.top", "port": 25569},
    "Survival": {"ip": "in.leoxstudios.com", "port": 10007}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    stats = {}
    for server_name, server_info in SERVERS.items():
        try:
            server = JavaServer(server_info["ip"], server_info["port"])
            status = server.status()
            stats[server_name] = {
                "online": True,
                "players": status.players.online,
                "max_players": status.players.max
            }
        except:
            stats[server_name] = {
                "online": False,
                "players": 0,
                "max_players": 0
            }
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
