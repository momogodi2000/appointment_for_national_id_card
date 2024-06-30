document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.corps-card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            alert('More details about ' + this.querySelector('.corps-card-title').textContent);
        });
    });
});