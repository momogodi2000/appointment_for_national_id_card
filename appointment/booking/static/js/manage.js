function deleteContact(contactId) {
    if (confirm('Are you sure you want to delete this contact?')) {
        $.ajax({
            url: '/delete-contact/' + contactId + '/',
            method: 'DELETE',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            success: function(response) {
                location.reload(); // Reload page on success
            },
            error: function(xhr, status, error) {
                console.error('Failed to delete contact:', error);
            }
        });
    }
}
