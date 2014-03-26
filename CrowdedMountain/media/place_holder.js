; $(document).ready(function(){
    //this code is executed after the DOM is completely loaded, 
    //  use the immediately indiced function experessions to do otherwise.
    $('nav a, footer a.up').click(function(e){
	
	//if a link is clicked somewhere scroll the page to that link's hash
	$.scrollTo( this.hash || 0, 1500 );
	e.preventDefault();
    });
});
