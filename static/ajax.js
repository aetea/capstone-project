
// ============== Search Functions =================

// function to change the url
function changeUrl(title, url) {
    if ( typeof(history.pushState) != "undefined") {
        let obj = { Title: title, Url: url };
        history.pushState(obj, obj.Title, obj.Url)
    }
};


// add listener to search box - when submit is clicked, do this 
$('#header-search').on('submit', (evt) => {
    evt.preventDefault();

    // get user input from the search box 
    const cityLookup = $('#header-search-box').val();
    
    // // send user-input to the server, get a Response, then do this 
    $.get("/api/city", {cname: cityLookup}, (res) => {
        // alert("hi from city api");
        console.log("response received by jquery:");
        console.log(res);

        // TODO: add error handling: if no city found/returned
        // might happen if non-city, or if db/teleport has no info

        // update page DOM to display response data  
        // TODO: should this all just be a separate HTML file? replace entire table
        $("#city-header").text(res.cityName); // TODO: make title case (from server)
        $("#country").text(`Country: ${res.country}`); // TODO: make title case
        $("#save-btn").html(`<button type="button" onclick="saveCity('${res.cityId}')">
                            Fav ${res.cityName}</button>`);
        
        // change URL 
        changeUrl(res.cityName, `/city-info/${res.cityName}`);
    });
});


// =============== Save Functions ================

// function to allow users to save city as a fav
// TODO: (v2) add functionality to save as "lived here previously"

function saveCity(cityId) {
    // add usercity to database [server POST request]
    console.log(`entered jsfunc saveCity with cityId: ${cityId}`);

    const connectionData = {
        "user": 1,      // TODO: make this handle a real user 
        "cityId": cityId
    };

    console.log(`sending connectionData as: ${connectionData}`)

    $.post("/save-city", connectionData, (res) => {
        if (res === "success") {
            alert(`Faved cityid: ${cityId}!`);
            // alert(`${res}`)
        } else {
            alert("Hi from save-city js. Save failed.");
        }
    });

    // update "save" element to indicate saved status [DOM]
};