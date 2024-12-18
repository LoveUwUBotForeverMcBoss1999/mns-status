// File: static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const searchResults = document.getElementById('searchResults');

    if (searchButton) {
        searchButton.addEventListener('click', performSearch);
    }

    if (searchInput) {
        searchInput.addEventListener('keyup', (event) => {
            if (event.key === 'Enter') {
                performSearch();
            }
        });
    }

    function performSearch() {
        const searchTerm = searchInput.value.trim();

        if (searchTerm.length < 2) {
            alert('Please enter at least 2 characters');
            return;
        }

        fetch(`/api/search?term=${encodeURIComponent(searchTerm)}`)
            .then(response => response.json())
            .then(results => {
                displaySearchResults(results);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while searching');
            });
    }

    function displaySearchResults(results) {
        if (!searchResults) return;

        searchResults.innerHTML = results.length ?
            results.map(island => `
                <div class="island-card" onclick="window.location.href='/island/${island.owner}'">
                    <img src="https://mc-heads.net/avatar/${island.name}" alt="${island.name}'s Avatar" class="avatar">
                    <div class="island-details">
                        <h2>${island.name || 'Unnamed Island'}</h2>
                        <p>Owner: ${island.name}</p>
                    </div>
                </div>
            `).join('') :
            '<p>No results found</p>';
    }
});