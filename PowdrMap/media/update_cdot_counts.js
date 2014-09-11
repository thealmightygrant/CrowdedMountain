; $(document).ready(function(){

    //this code is executed after the DOM is completely loaded, 
    //  use the immediately induced function expressions to do otherwise.

    var pages = ["#article1", "#article2", "#article3"],
    pN = pages.length,
    scrollingNow = false,
    last_anchor = -1,
    current_anchor = 0; // array position

    // Using the core $.ajax() method
    $.ajax({
	// the URL for the request
	// should the data be pulled directly from the database OR
	//   setup as JSON on another url
	url: "post.php",
	// the data to send (will be converted to a query string)
	data: {
	    id: 123
	},
	// whether this is a POST or GET request
	type: "GET",
	// the type of data we expect back
	dataType : "json",
	// code to run if the request succeeds;
	// the response is passed to the function
	success: function( json ) {
	    $( "<h1/>" ).text( json.title ).appendTo( "body" );
	    $( "<div class=\"content\"/>").html( json.html ).appendTo( "body" );
	},
	// code to run if the request fails; the raw request and
	// status codes are passed to the function
	error: function( xhr, status, errorThrown ) {
	    alert( "Sorry, there was a problem!" );
	    console.log( "Error: " + errorThrown );
	    console.log( "Status: " + status );
	    console.dir( xhr );
	},
	// code to run regardless of success or failure
	complete: function( xhr, status ) {
	    alert( "The request is complete!" );
	}
    });

});
