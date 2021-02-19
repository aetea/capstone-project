// [ajax] when form is submitted, do the following:
// stop default action
// update the url
// send search to server and get results
// display results on this page


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

        // TODO: add error handling: if no city found/returned
        // might happen if non-city, or if db/teleport has no info

        // update page DOM to display response data  
        $("#city-header").text(res.cityName); // TODO: make title case (from server)
        $("#country").text(res.country); // TODO: make title case
        
        // change URL 
        changeUrl(res.cityName, `/city-info/${res.cityName}`);
    });
    
    
});
