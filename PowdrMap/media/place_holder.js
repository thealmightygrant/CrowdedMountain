; $(document).ready(function(){

    
    var pages = ["#article1", "#article2", "#article3"],
    pN = pages.length,
    scrollingNow = false,
    a = 0; // array position


    $(window).on("wheel WheelEvent", function(e){
	
	if(scrollingNow === false){
	    scrollingNow = true;

	    var delta = parseInt(e.originalEvent.deltaY);
	    
	    delta < 0 ? --a : ++a;
	    if (a >= pN ) {
		a = (pN - 1);
	    }
	    if ( a < 0 ) {
		a = 0;
	    }

	    //if the mouse is scrolled, scroll the page to that link's hash
	    $( pages[a] ).ScrollTo({
		duration: 1000,
		callback: function(){
		    scrollingNow = false;
		}
	    });
	}
	e.preventDefault();
	
    });

    //Code to change the format of the nav section depending on the section being presented
    /*$('article').hover(
	function(e) {
	    //$("a[href='" +  +"']").addClass("in_view");
	}, function(e) {
	    $( this ).find( "span:last" ).remove();
	}
    });*/

    //this code is executed after the DOM is completely loaded, 
    //  use the immediately induced function expressions to do otherwise.
    $('nav a, footer a.up').click(function(e){
	
	//if a link is clicked somewhere scroll the page to that link's hash
	$( this.hash ).ScrollTo({
	    duration: 1000
	    //onlyIfOutside: true
	    //easing: 'linear'
	});

	e.preventDefault();
    });
});
