document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.contact-form');
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Empêche l'envoi par défaut du formulaire

        const formData = new FormData(form);  // Récupère les données du formulaire

        // Envoi des données du formulaire via fetch
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'  // Pour indiquer une requête AJAX
            }
        })
        .then(response => response.json())  // Parse la réponse JSON
        .then(data => {
            // Supprimer les anciens messages s'ils existent
            const existingMessage = form.querySelector('.form-message');
            if (existingMessage) {
                existingMessage.remove();
            }

            // Créer un élément <p> pour le message
            const message = document.createElement('p');
            message.classList.add('form-message');  // Ajouter une classe pour le style
            
            if (data.message) {
                message.textContent = data.message;
                message.style.color = 'green';
            } else if (data.errors) {
                message.textContent = 'Il y a eu des erreurs dans votre soumission : ' + JSON.stringify(data.errors);
                message.style.color = 'red';
            }
            
            // Appliquer des styles au message
            message.style.fontStyle = 'italic';

            // Ajouter le message en bas du formulaire
            form.appendChild(message);
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    });
});
