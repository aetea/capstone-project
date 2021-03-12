
// =============== Save Functions ================

function popLocalToast() {
};

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
            $("#save-elements").attr("class", "hide");
            $("#unsave-elements").attr("class", "show");
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
            $("#save-elements").attr("class", "show");
            $("#unsave-elements").attr("class", "hide");
            // $("#pastlocal-div").attr("class", "hide");
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

