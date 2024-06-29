$(document).ready(function() {
    $('.btn-primary').hover(
        function() {
            $(this).animate({ backgroundColor: "#0056b3", borderColor: "#004085" }, 300);
        },
        function() {
            $(this).animate({ backgroundColor: "#007bff", borderColor: "#007bff" }, 300);
        }
    );
});
