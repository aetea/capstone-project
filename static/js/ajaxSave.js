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
            // $("#past-local-set").addClass("hide");
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



// ============ Event Listeners ==========

// listen for save-form submit
$("#save-btn").on("click", saveCityProcess);
$("#past-local-box").on("change", saveCityProcess);