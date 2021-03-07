alert("hi from cityMap.js");

// =========  simple no-geolocation map  ============
// centered on this city (and has places search?)

let pos;
let map;
function initMap() {
    bounds = new google.maps.LatLngBounds();
    console.log(`lat is ${cityLat}, lon is ${cityLon}`);
    // pos = {lat: 37.601773, lng: -122.202870}; 
    pos = {lat: cityLat, lng: cityLon};
    map = new google.maps.Map(
        document.querySelector("#map"), {
            center: pos,
            zoom: 10
        });
        
    // Call Places Nearby Search on this location
    // getNearbyPlaces(pos);
  }

// Perform a Places Nearby Search Request
function getNearbyPlaces(position) {
    let request = {
    location: position,
    rankBy: google.maps.places.RankBy.DISTANCE,
    keyword: 'sushi'
    };

    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, nearbyCallback);
}

// Handle the results (up to 20) of the Nearby Search
function nearbyCallback(results, status) {
    if (status == google.maps.places.PlacesServiceStatus.OK) {
    createMarkers(results);
    }
}

// Set markers at the location of each place result
function createMarkers(places) {
    places.forEach(place => {
    let marker = new google.maps.Marker({
        position: place.geometry.location,
        map: map,
        title: place.name
    });

    /* TODO: Step 4B: Add click listeners to the markers */

    // Adjust the map bounds to include the location of this marker
    bounds.extend(place.geometry.location);
    });
    // Once all the markers have been placed, adjust the bounds of the map to
    // show all the markers within the visible area. 
    map.fitBounds(bounds);
}

/* TODO: Step 4C: Show place details in an info window */