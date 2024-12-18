import os
from flask import Flask, render_template, request, jsonify
from mcstatus import JavaServer
from database import DatabaseConnection

# Load environment variables or use defaults
PROXY_SERVER = os.getenv('PROXY_SERVER', 'panel2.mcboss.top')
PROXY_PORT = int(os.getenv('PROXY_PORT', 25565))

# Server configurations
SERVERS = {
    "Proxy": {"ip": "panel2.mcboss.top", "port": 25565},
    "Hub": {"ip": "panel2.mcboss.top", "port": 25567},
    "SkyBlock": {"ip": "panel2.mcboss.top", "port": 25570},
    "LifeSteal": {"ip": "panel2.mcboss.top", "port": 25566},
    "SkyWars": {"ip": "panel2.mcboss.top", "port": 25569},
    "Survival": {"ip": "in.leoxstudios.com", "port": 10007}
}

app = Flask(__name__)

# Configure Flask environment
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_secret_key_here')

def get_server_status(server_ip, server_port):
    """
    Helper function to get server status
    """
    try:
        server = JavaServer(server_ip, server_port)
        status = server.status()
        return {
            "online": True,
            "players": status.players.online,
            "max_players": status.players.max
        }
    except Exception as e:
        print(f"Error checking server status for {server_ip}:{server_port} - {e}")
        return {
            "online": False,
            "players": 0,
            "max_players": 0
        }

@app.route('/')
def index():
    proxy_status = get_server_status(PROXY_SERVER, PROXY_PORT)
    return render_template('index.html', 
                         proxy_players=proxy_status['players'],
                         proxy_max_players=proxy_status['max_players'])

@app.route('/api/stats')
def get_stats():
    stats = {"Proxy": get_server_status(PROXY_SERVER, PROXY_PORT)}

    # Get other servers' stats
    for server_name, server_info in SERVERS.items():
        if server_name != "Proxy":
            stats[server_name] = get_server_status(server_info["ip"], server_info["port"])
    
    return jsonify(stats)

@app.route('/sb-status')
def sb():
    """
    Render homepage with top 3 islands
    """
    db = DatabaseConnection()
    top_islands = db.get_top_islands(limit=3)
    db.close()
    return render_template('sb.html', islands=top_islands)

@app.route('/search')
def search():
    """
    Render search page
    """
    return render_template('search.html')

@app.route('/api/search')
def api_search():
    """
    API endpoint for searching islands
    """
    search_term = request.args.get('term', '')
    db = DatabaseConnection()
    results = db.search_islands(search_term)
    db.close()
    return jsonify(results)

@app.route('/island/<owner>')
def island_details(owner):
    """
    Render island details page for a specific owner
    """
    db = DatabaseConnection()
    island = db.get_island_by_owner(owner)
    db.close()
    return render_template('island_details.html', island=island)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
