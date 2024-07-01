$(document).ready(function() {
    $('.menu-toggle').on('click', function() {
        $('.dashboard-nav').toggleClass('active');
    });
});




// Custom JavaScript for Modal and Form Validation

$(document).ready(function() {
    // Form validation
    (function() {
        'use strict';
        window.addEventListener('load', function() {
            var forms = document.getElementsByClassName('needs-validation');
            var validation = Array.prototype.filter.call(forms, function(form) {
                form.addEventListener('submit', function(event) {
                    if (form.checkValidity() === false) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }, false);
            });
        }, false);
    })();

    // Modal for displaying found ID cards
    $('#idCardModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var modal = $(this);
    });
});
