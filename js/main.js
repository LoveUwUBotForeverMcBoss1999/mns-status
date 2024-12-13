// main.js
window.onload = function() {
    fetch('http://panel2.mcboss.top:25565/status')
        .then(response => response.json())
        .then(data => {
            const playerCountElement = document.getElementById('player-count');
            const currentPlayers = data.current_players;
            const maxPlayers = data.max_players;

            playerCountElement.textContent = `${currentPlayers} / ${maxPlayers}`;
        })
        .catch(error => {
            console.error('Error fetching player count:', error);
        });
};
