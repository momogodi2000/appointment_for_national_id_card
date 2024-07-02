document.addEventListener("DOMContentLoaded", function() {
    const menuToggle = document.querySelector(".menu-toggle");
    const dashboardNav = document.querySelector(".dashboard-nav");

    menuToggle.addEventListener("click", function() {
        dashboardNav.classList.toggle("active");
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const menuToggle = document.querySelector(".menu-toggle");
    const dashboardNav = document.querySelector(".dashboard-nav");

    menuToggle.addEventListener("click", function() {
        dashboardNav.classList.toggle("active");
    });

    document.querySelectorAll(".dashboard-nav-item").forEach(function(item) {
        item.addEventListener("mouseover", function() {
            item.classList.add("hover");
        });
        item.addEventListener("mouseout", function() {
            item.classList.remove("hover");
        });
    });
});
