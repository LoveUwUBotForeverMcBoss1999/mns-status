from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# List of servers and their IPs
servers = [
    {"name": "SkyBlock", "uuid": "d6cd4493-378f-47f2-b6e0-6c8d13018ce5", "ip": "panel2.mcboss.top", "port": 25570},
    {"name": "LifeSteal", "uuid": "db967e1a-9477-451b-b92d-f022d5b2fd1b", "ip": "panel2.mcboss.top", "port": 25566},
    {"name": "Hub", "uuid": "77664d0d-24db-4639-977a-6fcb07b08017", "ip": "panel2.mcboss.top", "port": 25567},
    {"name": "Proxy", "uuid": "a5479a08-c4b7-4c96-9c30-8ad2073c8864", "ip": "panel2.mcboss.top", "port": 25565},
    {"name": "SkyWars", "uuid": "09afc51b-325c-4bea-b68c-3e7603e8b9a4", "ip": "panel2.mcboss.top", "port": 25569},
    {"name": "Survival", "uuid": "5dcd834d-72d6-49d0-b3fc-a6eb299c43af", "ip": "in.leoxstudios.com", "port": 10007},
]

# Function to fetch server status (you might need to adjust this based on actual API or status check)
def get_server_status(ip, port):
    try:
        response = requests.get(f'http://{ip}:{port}/status')  # Assuming an API that provides status (you can adjust this)
        data = response.json()
        return data
    except:
        return None

@app.route('/')
def index():
    server_stats = []
    
    for server in servers:
        status = get_server_status(server['ip'], server['port'])
        if status:
            server_stats.append({
                "name": server['name'],
                "uuid": server['uuid'],
                "status": "Online" if status['online'] else "Stopped",  # Assuming 'online' key exists
                "current_players": status['current_players'],  # Assuming 'current_players' exists
                "max_players": status['max_players']  # Assuming 'max_players' exists
            })
        else:
            server_stats.append({
                "name": server['name'],
                "uuid": server['uuid'],
                "status": "Stopped",
                "current_players": 0,
                "max_players": 0
            })
    
    return render_template('index.html', server_stats=server_stats)

if __name__ == '__main__':
    app.run(debug=True)
