
    let map, service, infowindow, directionsService, directionsRenderer;

    function initMap() {
        // Initialize the map
        map = new google.maps.Map(document.getElementById('map'), {
            center: { lat: -34.397, lng: 150.644 },
            zoom: 15,
            mapTypeId: 'roadmap'
        });

        directionsService = new google.maps.DirectionsService();
        directionsRenderer = new google.maps.DirectionsRenderer();
        directionsRenderer.setMap(map);

        // Info window
        infowindow = new google.maps.InfoWindow();

        document.getElementById('locate-btn').addEventListener('click', () => {
            locateMe();
        });
    }

    function locateMe() {
        // Display loader
        document.getElementById('loader').style.display = 'block';

        // Geolocation
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    map.setCenter(pos);
                    findNearbyPoliceStations(pos);

                    // Hide loader
                    document.getElementById('loader').style.display = 'none';
                },
                () => {
                    handleLocationError(true, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, map.getCenter());
        }
    }

    function handleLocationError(browserHasGeolocation, pos) {
        infowindow.setPosition(pos);
        infowindow.setContent(
            browserHasGeolocation
                ? 'Error: The Geolocation service failed.'
                : 'Error: Your browser doesn\'t support geolocation.'
        );
        infowindow.open(map);

        // Hide loader
        document.getElementById('loader').style.display = 'none';
    }

    function findNearbyPoliceStations(location) {
        const request = {
            location: location,
            radius: '5000', // Search within 5km radius
            type: ['police']
        };

        service = new google.maps.places.PlacesService(map);
        service.nearbySearch(request, (results, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                for (let i = 0; i < results.length; i++) {
                    createMarker(results[i]);

                    if (i === 0) {
                        // Show the route to the first police station found
                        showRoute(location, results[i].geometry.location);
                    }
                }
            } else {
                alert('No nearby police stations found.');
            }
        });
    }

    function createMarker(place) {
        const marker = new google.maps.Marker({
            map: map,
            position: place.geometry.location,
            title: place.name
        });

        google.maps.event.addListener(marker, 'click', () => {
            infowindow.setContent(place.name + '<br>' + place.vicinity);
            infowindow.open(map, marker);
        });
    }

    function showRoute(origin, destination) {
        const request = {
            origin: origin,
            destination: destination,
            travelMode: google.maps.TravelMode.DRIVING
        };

        directionsService.route(request, (result, status) => {
            if (status === google.maps.DirectionsStatus.OK) {
                directionsRenderer.setDirections(result);
            } else {
                alert('Could not display route.');
            }
        });
    }

    // Initialize the map on page load
    window.onload = initMap;
