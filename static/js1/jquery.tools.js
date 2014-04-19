
/* navigation */

var navigation = function()
{
	var thisID = null;

	$( 'a#about, a#work' ).click( function()
	{
		thisID = this.id;
		
		$( '#content' ).animate( { height: getPageHeight() }, 700, function()
		{
			$( '#content-inner-1' ).addClass( 'footer-' + thisID ).fadeIn( 500 );
			$( '#content-' + thisID ).fadeIn( 500, function()
			{
				$( 'a#close' ).fadeIn( 300 );
			});
		});

		return false;
	});

	$( 'a#close' ).click( function()
	{
		$( this ).fadeOut( 300, function()
		{
			$( '#content-inner-1' ).fadeOut( 400, function()
			{
				$( this ).removeClass( 'footer-' + thisID );
				$( '#content-' + thisID ).hide();
				$( '#content' ).animate( { height: 0 }, 700, function()
				{
					$( this ).hide();
				});
			});
		});

		return false;
	});
};

$( window ).load( navigation );


/* moreLess: show and hide content */

var moreLess = function()
{
	var targetClass	= $( '.more-box' );
	var linkClass	= $( 'a.more-link' );

	linkClass.click( function()
	{
		var box = $( '#' + this.id + '-box' );

		if( box.is( ':hidden' ) )
		{
			box.slideDown( 1000 );
			$( this ).children( 'span.more' ).hide();
			$( this ).children( 'span.less' ).show();
		}
		else
		{
			box.slideUp( 1000 );
			$( this ).children( 'span.more' ).show();
			$( this ).children( 'span.less' ).hide();
		}

		return false;
	});
};

$( window ).load( moreLess );


/* workShowcase */

var workShowcase = function()
{
	var works		= $( '.item-box' );
	var catLinks	= $( 'a.work-cat' );
	var lists		= $( 'ul.work-list' );
	var curWorkPos	= $( 'b#work-current' );
	var worksCount	= $( 'span#works-count' );
	var currentList = $( 'ul#work-1-list' );
	var currentItem	= $( 'li#item-49' );
	var buttonNext	= $( 'a#work-next' );
	var buttonPrev	= $( 'a#work-prev' );
	var curItemTime = 0;

	worksCount.html( currentList.children().length );

	catLinks.click( function()
	{
		catLinks.removeClass( 'button-selected' );
		$( '#' + this.id ).addClass( 'button-selected' );

		currentList = $( '#' + this.id + '-list' );
		lists.each( function()
		{
			if( !$( this ).is( ':hidden' ) )
			{
				$( this ).fadeOut( 300, function()
				{
					currentList.fadeIn( 300 );
				});
				return false;
			}
		});

		currentItem = currentList.children( 'li:first' );
		updateItemBox( false );
		updateList();
		updateItemPos();
		worksCount.text( currentList.children().length );

		return false;
	});

	lists.children( 'li' ).click( function()
	{
		currentItem = $( this );
		updateItemBox();
		updateList();
		updateItemPos();

		return false;
	});

	buttonNext.click( function()
	{
		if( duplicatePrevention() == true )
			return false;

		var tmp = currentItem.next();
		if( !tmp.attr( 'id' ) )
			tmp = currentList.children( 'li:first' );
	
		currentItem = tmp;
		updateItemBox();
		updateList();
		updateItemPos();

		return false;
	});

	buttonPrev.click( function()
	{
		if( duplicatePrevention() == true )
			return false;

		var tmp = currentItem.prev();
		if( !tmp.attr( 'id' ) )
			tmp = currentList.children( 'li:last' );
	
		currentItem = tmp;
		updateItemBox();
		updateList();
		updateItemPos();

		return false;
	});


	function updateItemBox( scrollTo )
	{
		works.each( function()
		{
			var box = $( '#' + currentItem.attr( 'id' ) + '-box' );

			if( !box.attr( 'id' ) )
				return false;

			if( !$( this ).is( ':hidden' ) )
			{
				$( this ).fadeOut( 300, function()
				{
					box.fadeIn( 300, function()
					{
						if( scrollTo != false )
							$( 'html, body' ).animate( { scrollTop: $( '#work-current' ).offset().top - 50 }, 300 );
					});
				});
				return false;
			}
		});
	}

	function updateList()
	{
		currentList.children( 'li' ).removeClass( 'selected' );
		currentItem.addClass( 'selected' );
	}

	function updateItemPos()
	{
		var pos = 0;
		currentList.children().each( function( i )
		{
			if( this.id == currentItem.attr( 'id' ) )
			{
				pos = i + 1;
				return false;
			}
		});
		curWorkPos.text( pos );

		if( worksCount.text() == pos )
		{
			for( i = 0; i < 5; i++ )
				curWorkPos.fadeOut( 200 ).fadeIn( 200 );
		}
	}

	function duplicatePrevention()
	{
		ret = false;

		mc = new Date();
		if( curItemTime != 0 )
		{
			diff = mc.getTime() - curItemTime;
			if( ( diff / 600 ) < 1 )
				ret = true;
		}

		if( ret == false )
			curItemTime = mc.getTime();

		return ret;
	}
};

$( window ).load( workShowcase );


/* contact form */

var contactForm = function()
{
	var respObj	= $( 'p#contact-response' );
	var msgObj	= $( 'textarea#f-text' );

	$( 'form#contact-form' ).submit( function()
	{
		respObj.html( '<i>Please wait...</i>' ).show();

		jQuery.ajax(
		{
			url: 		this.action,
			type:		this.method,
			data: 		'message=' + msgObj.val(),
			dataType: 	'json',
			timeout: 	2000,
			error: function() 
			{
				respObj.fadeOut( 150, function()
				{
					respObj.fadeIn( 300 ).html( '<span class="red">Oops!</span> An unknown error, sorry.. Try again, please!' );
				});
			},
			success: function( data ) 
			{
				respObj.fadeOut( 150, function()
				{
					respObj.fadeIn( 300 ).html( data.response );
				});

				if( data.success == true )
					msgObj.val( '' );
			}
		});

		return false;
	});
};

$( window ).load( contactForm );


/* twitter */

var twitterCorner = function()
{
	var linkObj	= $( '#twitter-corner a' );
	var infoObj	= $( '#twitter-corner div' );

	linkObj.hover( function()
	{
		infoObj.fadeIn( 300 ).animate( { 'right' : '45px' }, 300 );
	}, 
	function()
	{
		infoObj.animate( { 'right' : '65px' }, 300 ).fadeOut( 300 );
	});

};

$( window ).load( twitterCorner );


/* functions */

function getPageHeight() 
{
	var windowHeight;

	if( self.innerHeight )
		windowHeight = self.innerHeight;

	else if( document.documentElement && document.documentElement.clientHeight )
		windowHeight = document.documentElement.clientHeight;

	else if( document.body )
		windowHeight = document.body.clientHeight;

	return windowHeight;
}
