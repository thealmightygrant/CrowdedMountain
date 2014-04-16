; $(document).ready(function(){

    //this code is executed after the DOM is completely loaded, 
    //  use the immediately induced function expressions to do otherwise.

    var pages = ["#article1", "#article2", "#article3"],
    pN = pages.length,
    scrollingNow = false,
    lasta = -1,
    a = 0; // array position

    $(window).on("wheel WheelEvent", function(e){
	
	if(scrollingNow === false){
	    scrollingNow = true;

	    var delta = parseInt(e.originalEvent.deltaY);
	    
	    lasta = a;
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
		    //call nav change function
		    if (lasta != a){
			$('#nav_' + lasta).addClass('in_view');
			$('#nav_' + a).removeClass('in_view');
		    }
		}
	    });
	}
	e.preventDefault();
	
    });
    
    //if a link is clicked somewhere scroll the page to that link's hash
    $('nav a').click(function(e){
	if(scrollingNow == false){
	    var link_name = $(this).attr("href");
	    $( link_name ).ScrollTo({
		duration: 1000,
		callback: function(){
		    scrollingNow = false;
		    //call nav change function
		    $('a[href=' + link_name + ']').addClass('in_view');
		    $('a').not('[href=' + link_name + ']').removeClass('in_view');

		    //set a
		}
	    });

	    e.preventDefault();
	}
    });
});
