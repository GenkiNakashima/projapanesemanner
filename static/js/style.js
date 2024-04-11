$(window).scroll(function(){
  if ($(window).scrollTop() >= 300) {
      $('nav').addClass('fixed-header');
      $('nav div').addClass('visible-title');
  }
  else {
      $('nav').removeClass('fixed-header');
      $('nav div').removeClass('visible-title');
  }
});

$(function() {
  $('.slick').slick({
      fade: true,
      autoplay: true,
      speed: 1500,
      autoplaySpeed : 2000,
      pauseOnFocus: false,
      pauseOnHover: false,
      arrows: false,
  })
});
