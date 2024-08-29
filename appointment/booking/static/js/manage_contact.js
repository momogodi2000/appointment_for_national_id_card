// Initialize Bootstrap tooltips (optional)
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

// Handle Reply Modal
$('#replyModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var email = button.data('email'); // Extract info from data-* attributes

    // Update the modal's content
    var modal = $(this);
    modal.find('#contactEmail').val(email);
});

// Delete Contact Function
function deleteContact(contactId) {
    if (confirm('Are you sure you want to delete this contact message?')) {
        // You may use AJAX to send a delete request to the server
        // Example: $.post('/delete_contact/', { id: contactId });
        window.location.href = `/delete_contact/${contactId}/`;
    }
}
