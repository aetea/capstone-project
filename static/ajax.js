
// =============== Save Functions ================

// function to save city
function saveCity(userId, cityId, pastLocal) {
    const connectionData = {};
    
    // do something
};


// function to unsave city
function unsaveCity(userId, cityId) {
    const connectionData = {
        "unsave-btn": cityId,
        "user-id": userId
    };

    $.post("/unsave-city", connectionData, (res) => {      // callback function
        if (res === "success") {
            // update button and text
            $("#save-btn").attr("class", "show");
            $("#unsave-btn").attr("class", "hide");
        } else {
            alert("uhoh! sorry, that did not work");
        };
    });

};


// ============ Save/Unsave Event Listeners ==========

// listen for save-form submit
$("#save-btn").on("submit", (evt) => {        // callback function
    evt.preventDefault();

    // get userId, cityId, pastLocal status from form/page
    // run saveCity function 

});

// listen for unsave-form submit 
$("#unsave-btn").on("click", (evt) => {      // callback function
    // thing to do 
    evt.preventDefault(); 

    // todo show warning 
    // const userId = $("#header-profile").attr("name");
    const cityId = $(evt.target).attr("value");
    const userId = $("#h-uid").attr("value");

    // get userid and cityid from form/page
    console.log(`user is ${userId}`);
    console.log(`city is ${cityId}`);

    // console.log("do you want to run the unsave function now?");
    unsaveCity(userId, cityId);

});





// ============== OLD FUNCTIONS ================

// function to allow users to save city as a fav

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