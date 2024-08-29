document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const dashboardNav = document.querySelector(".dashboard-nav");

    menuToggle.addEventListener("click", function () {
        dashboardNav.classList.toggle("open");
    });
});

// Add this to your existing JavaScript file

// Get the dashboard nav and toolbar elements
const dashboardNav = document.querySelector('.dashboard-nav');
const dashboardToolbar = document.querySelector('.dashboard-toolbar');
const menuToggle = document.querySelector('.menu-toggle');

// Add event listener to the menu toggle button
menuToggle.addEventListener('click', () => {
  // Toggle the 'closed' class on the dashboard nav
  dashboardNav.classList.toggle('closed');
});

// Add event listener to the dashboard nav
dashboardNav.addEventListener('transitionend', () => {
  // If the dashboard nav is closed, add the 'closed' class to the dashboard toolbar
  if (dashboardNav.classList.contains('closed')) {
    dashboardToolbar.classList.add('closed');
  } else {
    dashboardToolbar.classList.remove('closed');
  }
});

// Add this to your existing Chart.js script

// Animate the chart
myChart.options.animation = {
    duration: 1000,
    easing: 'easeInOutQuart',
    onComplete: () => {
      // Animate the chart when the animation is complete
      myChart.options.animation.onComplete = null;
    }
  };