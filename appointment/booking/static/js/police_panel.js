document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const dashboardNav = document.querySelector(".dashboard-nav");

    menuToggle.addEventListener("click", function () {
        dashboardNav.classList.toggle("open");
    });
});
