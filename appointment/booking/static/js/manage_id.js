// Handle Delete ID Card Function
function deleteIDCard(idCardId) {
    if (confirm('Are you sure you want to delete this missing ID card record?')) {
        // You may use AJAX to send a delete request to the server
        // Example: $.post('/delete_id_card/', { id: idCardId });
        window.location.href = `/delete_id_card/${idCardId}/`;
    }
}
