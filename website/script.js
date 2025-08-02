// SpydirWebz Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('🕷️ SpydirWebz website loaded');
    
    // Add any main page interactions here
    const puzzleCards = document.querySelectorAll('.puzzle-card');
    puzzleCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.classList.contains('play-button')) {
                const link = this.querySelector('.play-button');
                if (link) {
                    window.location.href = link.href;
                }
            }
        });
    });
});