;( function( $, window, undefined ) {

    //strict mode can run faster than regular javascript
    //strict mode eliminates some silent errors and makes them throw
    'use strict';

    //declare a function named MountainSlider
    //we are declaring the property jQuery.MountainSlider

    $.MountainSlider = function( options, element ) {
	//any element that is passed in will be accessible as this.$el
        this.$el = $( element );
	//we pass any options to the existing jquery init function
        this._init( options );
    };

    $.MountainSlider.prototype = {

	_init : function( options ) {
	    
	    //overload the _init function so that it does what we desire
	    
	    // the categories are the ul members 
	    this.$categories = this.$el.children('ul');
	    
	    //the navigation
	    this.$navcategories = this.$el.find('nav > a');
	    
	    /*var popup_info = "";

	    for (var i=0; i < this.$categories.length; i++)
	    {
		popup_info += this.$categories[i];
	    }

	    alert(popup_info);*/

	    //declare variables that end animations
	    var animEndEventNames = {
		'WebkitAnimation' : 'webkitAnimationEnd',
		'OAnimation' : 'oAnimationEnd',
		'msAnimation' : 'MSAnimationEnd',
		'animation' : 'animationend'
	    };
	    
	    // animation end event name
	    this.animEndEventName = animEndEventNames[ Modernizr.prefixed( 'animation' )];

	    // animations and transforms support
	    this.support = Modernizr.csstransforms && Modernizr.cssanimations;

	    // if currently animating
	    this.isAnimating = false;

	    //current category
	    this.current = 0;
	    var $currcat = this.$categories.eq(0);
	    
	    if( !this.support ){
		this.$categories.hide();
		$currcat.show()
	    }
	    else{
		$currcat.addClass('mountain-current');
	    }

	    //curent nav category
	    this.$navcategories.eq(0).addClass('mountain-selected');

	    //init events
	    this._initEvents();

	},
	_initEvents : function() {

            var self = this;
            this.$navcategories.on( 'click.mountainslider', function() {
                self.showCategory( $( this ).index() );
                return false;
            } );

            // reset on window resize..
            $( window ).on( 'resize', function() {
                self.$categories.removeClass().eq( 0 ).addClass( 'mountain-current' );
                self.$navcategories.eq( self.current ).removeClass( 'mountain-selected' ).end().eq( 0 ).addClass( 'mountain-selected' );
                self.current = 0;
            } );

        },
        showCategory : function( catidx ) {

            if( catidx === this.current || this.isAnimating ) {
                return false;
            }
            this.isAnimating = true;
            // update selected navigation
            this.$navcategories.eq( this.current ).removeClass( 'mountain-selected' ).end().eq( catidx ).addClass( 'mountain-selected' );

            var dir = catidx > this.current ? 'right' : 'left',
            toClass = dir === 'right' ? 'mountain-moveToLeft' : 'mountain-moveToRight',
            fromClass = dir === 'right' ? 'mountain-moveFromRight' : 'mountain-moveFromLeft',
            // current category
            $currcat = this.$categories.eq( this.current ),
            // new category
            $newcat = this.$categories.eq( catidx ),
            $newcatchild = $newcat.children(),
            lastEnter = dir === 'right' ? $newcatchild.length - 1 : 0,
            self = this;

            if( this.support ) {

                $currcat.removeClass().addClass( toClass );
                
                setTimeout( function() {

                    $newcat.removeClass().addClass( fromClass );
                    $newcatchild.eq( lastEnter ).on( self.animEndEventName, function() {

                        $( this ).off( self.animEndEventName );
                        $newcat.addClass( 'mountain-current' );
                        self.current = catidx;
                        var $this = $( this );
                        // solve chrome bug
                        self.forceRedraw( $this.get(0) );
                        self.isAnimating = false;

                    } );

                }, $newcatchild.length * 70 );

            }
            else {

                $currcat.hide();
                $newcat.show();
                this.current = catidx;
                this.isAnimating = false;

            }

        },
        // based on http://stackoverflow.com/a/8840703/989439
        forceRedraw : function(element) {
            if (!element) { return; }
            var n = document.createTextNode(' '),
            position = element.style.position;
            element.appendChild(n);
            element.style.position = 'relative';
            setTimeout(function(){
                element.style.position = position;
                n.parentNode.removeChild(n);
            }, 25);
        }

    }

    //we are adding the function mountainslider to the $.fn so that it is now a jQuery object method
    $.fn.mountainslider = function( options ) {
	//
        var instance = $.data( this, 'mountainslider' );
        if ( typeof options === 'string' ) {
            var args = Array.prototype.slice.call( arguments, 1 );
            this.each(function() {
                instance[ options ].apply( instance, args );
            });
        }
        else {
            this.each(function() {
                instance ? instance._init() : instance = $.data( this, 'mountainslider', new $.MountainSlider( options, this ) );
            });
        }
        return instance;
    };

} )( jQuery, window );
