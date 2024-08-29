document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.corps-card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            alert('More details about ' + this.querySelector('.corps-card-title').textContent);
        });
    });
});



// Chart.js script
var ctx = document.getElementById('statisticsChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Users', 'Appointments', 'Documents', 'Missing ID Cards', 'Notifications', 'Communications', 'Contact Us'],
        datasets: [{
            label: 'Counts',
            data: [
                {{ user_count }},
                {{ appointment_count }},
                {{ document_count }},
                {{ missing_id_card_count }},
                {{ notification_count }},
                {{ communication_count }},
                {{ contact_us_count }}
            ],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
