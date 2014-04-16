; $(document).ready(function(){

    //this code is executed after the DOM is completely loaded, 
    //  use the immediately induced function expressions to do otherwise.

    var pages = ["#article1", "#article2", "#article3"],
    pN = pages.length,
    scrollingNow = false,
    last_anchor = -1,
    current_anchor = 0; // array position

    $(window).on("wheel WheelEvent", function(e){
	
	if(scrollingNow === false){
	    scrollingNow = true;

	    var delta = parseInt(e.originalEvent.deltaY);
	    
	    last_anchor = current_anchor;
	    delta < 0 ? --current_anchor : ++current_anchor;
	    if (current_anchor >= pN ) {
		current_anchor = (pN - 1);
	    }
	    if ( current_anchor < 0 ) {
		current_anchor = 0;
	    }

	    //if the mouse is scrolled, scroll the page to that link's hash
	    $( pages[current_anchor] ).ScrollTo({
		duration: 1000,
		callback: function(){
		    scrollingNow = false;
		    //call nav change function
		    if (last_anchor != current_anchor){
			$('#nav_' + last_anchor).removeClass('in_view');
			$('#nav_' + current_anchor).addClass('in_view');
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

		    //set current_link for scrolling function
		    current_anchor = parseInt(link_name.charAt(link_name.length - 1)) - 1;
		}
	    });

	    e.preventDefault();
	}
    });
});
