// Add event listener to the form submit button
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form.needs-validation");
    const submitButton = form.querySelector("button[type='submit']");
  
    submitButton.addEventListener("click", function(event) {
      event.preventDefault();
  
      // Validate the form fields
      const nameInput = form.querySelector("input[name='name']");
      const emailInput = form.querySelector("input[name='email']");
      const messageInput = form.querySelector("textarea[name='message']");
  
      if (!nameInput.value) {
        nameInput.classList.add("is-invalid");
        return;
      }
  
      if (!emailInput.value || !emailInput.value.includes("@")) {
        emailInput.classList.add("is-invalid");
        return;
      }
  
      if (!messageInput.value) {
        messageInput.classList.add("is-invalid");
        return;
      }
  
      // If all fields are valid, submit the form
      form.submit();
    });
  });