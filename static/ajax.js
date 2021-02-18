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
    const cityName = $('#header-search-box').val();

    // change URL 
    changeUrl(cityName, `/city-info/${cityName}`);
    
    // // send user-input to the server, get a Response, then do this 
    $.get("/api/city", {cname: cityName}, (res) => {
        // alert("hi from city api");
        // update page DOM to display response data  
        $("#city-header").text(res.city_name); // TODO: make title case (from server)
        $("#country").text(res.country); // TODO: make title case
    });

});
