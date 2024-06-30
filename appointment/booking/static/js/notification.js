
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.notification-card');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            card.classList.add('read');
        });
    });
});

    document.addEventListener('DOMContentLoaded', function() {
        const cards = document.querySelectorAll('.notification-card');
        cards.forEach(card => {
            card.addEventListener('click', () => {
                card.classList.add('read');
                // Optionally, mark the notification as read on the server
                // You can make an AJAX request to update the notification status
            });
        });
    });



    document.addEventListener('DOMContentLoaded', function() {
        const cards = document.querySelectorAll('.notification-card');
        cards.forEach(card => {
            card.addEventListener('click', () => {
                card.classList.add('read');
                // Optionally, mark the notification as read on the server
                // You can make an AJAX request to update the notification status
            });
        });

        // Fetching notification data for chart
        const notificationData = {
            labels: {{ notification_labels|safe }},
            datasets: [{
                label: 'Notifications per Month',
                data: {{ notification_counts|safe }},
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth:
            }]
            };

        const ctx = document.getElementById('notificationChart').getContext('2d');
        const notificationChart = new Chart(ctx, {
            type: 'bar',
            data: notificationData,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });



    // notification.js
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.notification-card');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            card.classList.add('read');
            // Optionally, mark the notification as read on the server
            // You can make an AJAX request to update the notification status
        });
    });

    // Fetching notification data for chart
    const notificationData = {
        labels: JSON.parse(document.getElementById('notificationChart').dataset.labels),
        datasets: [{
            label: 'Notifications per Month',
            data: JSON.parse(document.getElementById('notificationChart').dataset.counts),
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    };

    const ctx = document.getElementById('notificationChart').getContext('2d');
    const notificationChart = new Chart(ctx, {
        type: 'bar',
        data: notificationData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

