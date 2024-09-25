// Get the dashboard nav and app elements
const dashboardNav = document.querySelector('.dashboard-nav');
const dashboardApp = document.querySelector('.dashboard-app');
const menuToggle = document.querySelector('.menu-toggle');

// Add event listener to the menu toggle button
menuToggle.addEventListener('click', () => {
    // Toggle the active class on the dashboard nav
    dashboardNav.classList.toggle('active');
    // Toggle the margin left on the dashboard app
    dashboardApp.classList.toggle('active');
});

// Add event listener to the window resize event
window.addEventListener('resize', () => {
    // Check if the window width is less than 768px
    if (window.innerWidth < 768) {
        // Hide the dashboard nav
        dashboardNav.style.display = 'none';
    } else {
        // Show the dashboard nav
        dashboardNav.style.display = 'block';
    }
});

// Add event listener to the dashboard nav to close it when clicking outside
document.addEventListener('click', (e) => {
    if (e.target !== menuToggle && e.target !== dashboardNav) {
        // Close the dashboard nav
        dashboardNav.classList.remove('active');
        dashboardApp.classList.remove('active');
    }
});