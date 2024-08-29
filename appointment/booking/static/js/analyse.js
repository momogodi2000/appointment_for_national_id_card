
// Fetch data and initialize charts
document.addEventListener("DOMContentLoaded", function() {
    // User Role Distribution Chart
    const ctxRole = document.getElementById('userRoleChart').getContext('2d');
    const userRoleChart = new Chart(ctxRole, {
        type: 'pie',
        data: {
            labels: ['User', 'Police Officer', 'Super Admin'],
            datasets: [{
                label: 'Role Distribution',
                data: {{ role_distribution|safe }},
                backgroundColor: ['#007bff', '#28a745', '#dc3545'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });

    // Appointment Status Distribution Chart
    const ctxStatus = document.getElementById('appointmentStatusChart').getContext('2d');
    const appointmentStatusChart = new Chart(ctxStatus, {
        type: 'doughnut',
        data: {
            labels: ['Created', 'Pending', 'Approved', 'Rejected'],
            datasets: [{
                label: 'Status Distribution',
                data: {{ status_distribution|safe }},
                backgroundColor: ['#ffc107', '#17a2b8', '#28a745', '#dc3545'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });

    // Display average appointments per officer
    document.getElementById('avgAppointments').innerText = "Average Appointments per Officer: {{ avg_appointments }}";
});
