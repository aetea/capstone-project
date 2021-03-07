
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
    zoom: 4,
    center: tpeCoords,
    });

    // new google.maps.Marker({
    //     position: tpeCoords,
    //     map: map,
    //     title: "Hello World!",
    // });

    // addSavedCities(userObj);

    let markers = []

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

        markers.push(marker)
    }

    // add listener and info
    for (const mark of markers) {
        const markerInfo = mark.title;
        const infoWindow = new google.maps.InfoWindow({
            content: markerInfo, 
            maxWidth: 200
        });

        console.log(mark.position);

        marker.addListener('click', () => {
            infoWindow.open(map, marker);
        });
    };
    
}

// ========== ADD USER SAVES FUNCTIONS ==============

function addSavedCities(user) {

    // get citylatlong and create markers
    for (const city of user["saved"]) {
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

        // // makeInfoWindow(marker)
        const markerInfo = marker.title;
        const infoWindow = new google.maps.InfoWindow({
            content: markerInfo, 
            maxWidth: 200
        });
        marker.addListener('click', () => {
            infoWindow.open(map, marker);
        });
    }

}

// set marker info and listener
// function makeInfoWindow(marker) {
//     const markerInfo = marker.title;
//     const infoWindow = new google.maps.InfoWindow({content:markerInfo});
//     marker.addListener('click', () => {infoWindow.open(map, marker);});
// }


// * differentiate general vs past_local
// use different markers for past vs general 

// ================= SUSHI CODE ===================
