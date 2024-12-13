from flask import Flask, render_template
import random

app = Flask(__name__)

# Sample data for the servers
servers = [
    {
        'name': 'SkyBlock',
        'uuid': 'd6cd4493-378f-47f2-b6e0-6c8d13018ce5',
        'owner': 'manu',
        'node': 'node1',
        'ip': 'panel2.mcboss.top:25570',
        'status': 'Online'  # Can be 'Online', 'Stopped', or 'Restarting'
    },
    {
        'name': 'LifeSteal',
        'uuid': 'db967e1a-9477-451b-b92d-f022d5b2fd1b',
        'owner': 'manu',
        'node': 'node1',
        'ip': 'panel2.mcboss.top:25566',
        'status': 'Stopped'
    },
    {
        'name': 'hub',
        'uuid': '77664d0d-24db-4639-977a-6fcb07b08017',
        'owner': 'manu',
        'node': 'node1',
        'ip': 'panel2.mcboss.top:25567',
        'status': 'Online'
    },
    {
        'name': 'Proxy',
        'uuid': 'a5479a08-c4b7-4c96-9c30-8ad2073c8864',
        'owner': 'manu',
        'node': 'node1',
        'ip': 'panel2.mcboss.top:25565',
        'status': 'Online',
        'members': random.randint(10, 100)  # Random member count for demonstration
    },
    {
        'name': 'SkyWars',
        'uuid': '09afc51b-325c-4bea-b68c-3e7603e8b9a4',
        'owner': 'manu',
        'node': 'node1',
        'ip': 'panel2.mcboss.top:25569',
        'status': 'Restarting'
    }
]

@app.route('/')
def index():
    return render_template('index.html', servers=servers)

if __name__ == '__main__':
    app.run(debug=True)
