// Affiche l'image suivante en changeant son style d'affichage
function showImage(element) {
    const nextElement = element.nextElementSibling;
    if (nextElement) {
        nextElement.style.display = 'block';
    }
}

// Cache l'image suivante en changeant son style d'affichage
function hideImage(element) {
    const nextElement = element.nextElementSibling;
    if (nextElement) {
        nextElement.style.display = 'none';
    }
}

// Incrémente le compteur de clics pour un animal spécifique
function incrementClick(animalId) {
    fetch(`/increment_click/${animalId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),  // Le corps de la requête est vide, car aucune donnée n'est envoyée
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Met à jour le texte du compteur de clics pour l'animal spécifié
        document.getElementById(`clicks-count-${animalId}`).textContent = data.new_click_count;
    })
    .catch((error) => {
        // Gère les erreurs et les affiche dans la console
        console.error('Error:', error);
    });
}
