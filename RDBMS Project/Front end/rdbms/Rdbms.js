$(document).ready(function() {
	$(window).scroll(function() {
  	if($(document).scrollTop() > 10) {
    	$('#nav1').addClass('shrink');
    	// $('#nav2').addClass('shrink');
    }
    else {
    $('#nav1').removeClass('shrink');
    // $('#nav2').removeClass('shrink');
    }
  });
	$('.nav li a').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'')
    && location.hostname == this.hostname) {
      var $target = $(this.hash);
      $target = $target.length && $target
      || $('[name=' + this.hash.slice(1) +']');
      if ($target.length) {
        var targetOffset = $target.offset().top;
        $('html,body')
        .animate({scrollTop: targetOffset}, 1200);
       return false;
      }
    }
  });
});
