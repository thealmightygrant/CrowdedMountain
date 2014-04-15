; $(document).ready(function(){

    
    /*var pages = ["#article1", "#article2", "#article3"],
    pN = pages.length,
    a = 0; // array position


    $('article').on("wheel WheelEvent", function(e){
    
	var delta = parseInt(e.originalEvent.deltaX || -e.originalEvent.detail, 10);
	
	delta<0 ? ++a : --a;
	a = a<0 ? pN-1 : a%pN; // loop pages array
	
	//if the mouse is scrolled, scroll the page to that link's hash
	$.scrollTo( pages[a] || 0, 1500 );
	e.preventDefault();
    
    });*/

    //this code is executed after the DOM is completely loaded, 
    //  use the immediately induced function experessions to do otherwise.
    $('nav a, footer a.up').click(function(e){
	
	//if a link is clicked somewhere scroll the page to that link's hash
	$.scrollTo( this.hash || 0, 1500 );
	e.preventDefault();
    });
});
