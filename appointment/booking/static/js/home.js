$(document).ready(function(){
    $('.procedure li').hover(
        function() {
            $(this).animate({ marginTop: "-=5px" }, 200);
        },
        function() {
            $(this).animate({ marginTop: "0px" }, 200);
        }
    );
});