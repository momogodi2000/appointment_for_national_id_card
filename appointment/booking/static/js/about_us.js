// Smooth scrolling for navigation links
$('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top
            }, 1000);
            return false;
        }
    }
});


// Scroll animation on page load
$(window).scroll(function() {
    $('.fade-in').each(function() {
        var top_of_element = $(this).offset().top;
        var bottom_of_window = $(window).scrollTop() + $(window).height();
        if (bottom_of_window > top_of_element) {
            $(this).animate({'opacity':'1'},500);
        }
    });
});


// Responsive navigation menu
$('#navbar-toggler').click(function() {
    $('#navbarResponsive').toggleClass('show');
});


// Launch modal for Project 1 live demo
$('#project1DemoBtn').click(function() {
    $('#project1Modal').modal('show');
 });
 