document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.contact-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Empêche l'envoi du formulaire pour cette démo

        // Créer un élément <p> pour le message
        const message = document.createElement('p');
        message.textContent = 'Votre message a été envoyé avec succès, a bientot !';
        
        // Appliquer des styles au message
        message.style.color = 'green';
        message.style.fontStyle = 'italic';
        
        // Ajouter le message en bas du formulaire
        form.appendChild(message);

        
    });
});
