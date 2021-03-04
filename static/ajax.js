
// =============== Save Functions ================

// function to send save city request to server 
function saveCityRequest(userId, cityId, isPastLocal) {
    const connectionData = {
        "connect_userid": userId,
        "save-city": cityId,
        "past_local": isPastLocal
    };

    console.log(`connectionData is ${connectionData}`);
    
    $.post("/save-city", connectionData, (res) => {
        if (res === "success") {
            // update button 
            $("#save-btn").attr("class", "hide");
            $("#unsave-btn").attr("class", "show");
            $("#pastlocal-div").attr("class", "show");
        } else {
            alert("uhoh! sorry, that did not work"); 
        };
    });
    
};


// function to evaluate save city form on page
function saveCityProcess(evt) {
    evt.preventDefault();
    
    // get userId, cityId, pastLocal status from form/page
    const cityId = $("#save-btn").attr("value");
    const userId = $("#h-uid").attr("value");
    console.log(`cityId is ${cityId}`)
    console.log(`userId is ${userId}`)
    
    // see if past_local checkbox is checked
    let isPastLocal = $("#past-local-box").prop("checked") === true;

    console.log(`isPastLocal is ${isPastLocal}`);     
    console.log("running save city...");   
    // run saveCity function 
    // saveCity(userId, cityId, isPastLocal);          

    // send request to server 
    saveCityRequest(userId, cityId, isPastLocal)
};


// function to unsave city
function unsaveCity(userId, cityId) {
    const connectionData = {
        "unsave-city": cityId,
        "user-id": userId
    };

    $.post("/unsave-city", connectionData, (res) => {      // callback function
        if (res === "success") {
            // update button
            $("#save-btn").attr("class", "show");
            $("#unsave-btn").attr("class", "hide");
        } else {
            alert("uhoh! sorry, that did not work");
        };
    });

};


// ============ Save/Unsave Event Listeners ==========

// listen for save-form submit
$("#save-btn").on("click", saveCityProcess);
$("#past-local-box").on("change", saveCityProcess);


// listen for unsave-form submit 
$("#unsave-btn").on("click", (evt) => {      // callback function
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

// function saveCity(cityId) {
//     // add usercity to database [server POST request]
//     console.log(`entered jsfunc saveCity with cityId: ${cityId}`);

//     const connectionData = {
//         "user": 1,      // TODO: make this handle a real user 
//         "cityId": cityId
//     };

//     console.log(`sending connectionData as: ${connectionData}`)

//     $.post("/save-city", connectionData, (res) => {
//         if (res === "success") {
//             alert(`Faved cityid: ${cityId}!`);
//             // alert(`${res}`)
//         } else {
//             alert("Hi from save-city js. Save failed.");
//         }
//     });

//     // update "save" element to indicate saved status [DOM]
// };