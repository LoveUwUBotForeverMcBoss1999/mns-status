from flask import Flask, render_template, jsonify
import socket
import json
from mcstatus import JavaServer

app = Flask(__name__)

PROXY_SERVER = "panel2.mcboss.top"
PROXY_PORT = 25565

SERVERS = {
    "Proxy": {"ip": "panel2.mcboss.top", "port": 25565},
    "Hub": {"ip": "panel2.mcboss.top", "port": 25567},
    "SkyBlock": {"ip": "panel2.mcboss.top", "port": 25570},
    "LifeSteal": {"ip": "panel2.mcboss.top", "port": 25566},
    "SkyWars": {"ip": "panel2.mcboss.top", "port": 25569},
    "Survival": {"ip": "in.leoxstudios.com", "port": 10007}
}

@app.route('/')
def index():
    try:
        proxy_server = JavaServer(PROXY_SERVER, PROXY_PORT)
        proxy_status = proxy_server.status()
        proxy_players = proxy_status.players.online
        proxy_max_players = proxy_status.players.max
    except:
        proxy_players = 0
        proxy_max_players = 0
    
    return render_template('index.html', 
                         proxy_players=proxy_players,
                         proxy_max_players=proxy_max_players)

@app.route('/api/stats')
def get_stats():
    stats = {}
    
    # Get proxy stats first
    try:
        proxy_server = JavaServer(PROXY_SERVER, PROXY_PORT)
        proxy_status = proxy_server.status()
        proxy_stats = {
            "online": True,
            "players": proxy_status.players.online,
            "max_players": proxy_status.players.max
        }
    except:
        proxy_stats = {
            "online": False,
            "players": 0,
            "max_players": 0
        }
    
    stats["Proxy"] = proxy_stats

    # Get other servers' stats
    for server_name, server_info in SERVERS.items():
        if server_name != "Proxy":  # Skip proxy as we already have it
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
