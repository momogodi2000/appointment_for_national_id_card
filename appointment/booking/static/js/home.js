// home.js

// Initialize and add the map
function initMap() {
    // Try to get the user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            // Map centered at user's location
            var map = new google.maps.Map(document.getElementById('map'), {
                zoom: 14,
                center: userLocation
            });

            // Place marker at user's location
            var marker = new google.maps.Marker({
                position: userLocation,
                map: map
            });

            // Find nearby police stations
            var service = new google.maps.places.PlacesService(map);
            service.nearbySearch({
                location: userLocation,
                radius: 5000,
                type: ['police']
            }, function(results, status) {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    for (var i = 0; i < results.length; i++) {
                        createMarker(results[i], map);
                    }
                }
            });

        }, function() {
            handleLocationError(true, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, map.getCenter());
    }
}

// Function to create a marker for each police station
function createMarker(place, map) {
    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });

    google.maps.event.addListener(marker, 'click', function() {
        var infowindow = new google.maps.InfoWindow();
        infowindow.setContent(place.name);
        infowindow.open(map, this);
    });
}

// Handle location errors
function handleLocationError(browserHasGeolocation, pos) {
    var infoWindow = new google.maps.InfoWindow({
        map: map,
        position: pos,
        content: browserHasGeolocation ?
            'Error: The Geolocation service failed.' :
            'Error: Your browser doesn\'t support geolocation.'
    });
}
