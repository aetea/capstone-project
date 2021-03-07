
// alert("hi from ajaxMap.js");

let pos;
let map;
let bounds;
let infoWindow;
let currentInfoWindow;
let service;
let infoPane;

// ================= SETUP MAP ====================
// =========== geolocation fanciness ==============
// \\ todo geolocate user

function initMap() {

    const LatLng = { lat: -25.363, lng: 131.044 };
    let tpeCoords = {lat: 25.04776, lng: 121.53185 };

    const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 1.5,
    center: tpeCoords,
    });
    
    markers = addSavedCities(userObj, map);
    addEventListeners(markers, map);    
    // ? --> have to manually pass map in, or markers don't appear. why? 
}

// ========== ADD USER SAVES FUNCTIONS ==============

function getCityPos(city) {
    console.log(city)

    let LatLongStr = city[4]   // string "(25.04776,121.53185)"
    let LatLong = LatLongStr.slice(1,-1).split(",");
    let coords = {lat: parseFloat(LatLong[0]), 
                  lng: parseFloat(LatLong[1]) };
    console.log(`coords ${coords["lat"]} ${coords["lng"]}`);

    return coords;
}

function addSavedCities(user, map) {

    let markers = [];

    for (const city of userObj["saved"]) {
        console.log(city)

        let LatLongStr = city[4]   // string "(25.04776,121.53185)"
        let LatLong = LatLongStr.slice(1,-1).split(",");
        let coords = {lat: parseFloat(LatLong[0]), lng: parseFloat(LatLong[1]) };
        console.log(`coords ${coords["lat"]} ${coords["lng"]}`);

        marker = new google.maps.Marker({
            position: coords,
            map: map, 
            title: city[0]
        }); 
        markers.push(marker);
    }

    return markers;
}

function addEventListeners(markers, map) {

    for (const mark of markers) {

        console.log(`now on ${mark.title} at ${mark.position.lat()}, 
                                             ${mark.position.lng()}`);

        const markerInfo = mark.title;
        const infoWindow = new google.maps.InfoWindow({
            content: markerInfo, 
            maxWidth: 200
        });

        mark.addListener('click', () => {
            infoWindow.open(map, mark);
            currentInfoWindow.close();
            currentInfoWindow = infoWindow;
        });
    };
}

// * differentiate general vs past_local
// use different markers for past vs general 

// ================= SUSHI CODE ===================
