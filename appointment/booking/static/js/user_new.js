
function initMap() {
    // Default location set to Yaoundé, Cameroon
    var defaultLocation = { lat: 3.8480, lng: 11.5021 };

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: defaultLocation
    });

    var marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        title: 'You are here'
    });

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            marker.setPosition(userLocation);
            map.setCenter(userLocation);

            // Example: Adding markers for nearby police stations (this could be dynamic based on API)
            var policeStations = [
                { lat: userLocation.lat + 0.01, lng: userLocation.lng + 0.01, name: 'Police Station 1' },
                { lat: userLocation.lat + 0.02, lng: userLocation.lng - 0.01, name: 'Police Station 2' },
            ];

            policeStations.forEach(function(station) {
                new google.maps.Marker({
                    position: { lat: station.lat, lng: station.lng },
                    map: map,
                    title: station.name
                });
            });
        });
    }
}

// Get the dashboard navigation and toolbar elements
const dashboardNav = document.querySelector('.dashboard-nav');
const dashboardToolbar = document.querySelector('.dashboard-toolbar');

// Add an event listener to the toolbar to toggle the sidebar
dashboardToolbar.addEventListener('click', () => {
// Toggle the open class on the toolbar
dashboardToolbar.classList.toggle('open');

// Update the width of the navigation
if (dashboardToolbar.classList.contains('open')) {
dashboardNav.style.width = '250px';
} else {
dashboardNav.style.width = '0px';
}
});

// Add an event listener to the window to update the navigation width on resize
window.addEventListener('resize', () => {
// Update the width of the navigation based on the screen size
if (window.innerWidth <= 768) {
dashboardNav.style.width = '200px';
} else if (window.innerWidth <= 480) {
dashboardNav.style.width = '150px';
} else {
dashboardNav.style.width = '250px';
}
});

