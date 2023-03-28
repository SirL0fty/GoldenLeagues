const navEl = document.querySelector('.navbar');

        window.addEventListener('scroll', () => {
                if (window.scrollY >= 70) {
                        navEl.classList.add('navbar-scrolled')
                } else if (window.scrollY < 70) {
                        navEl.classList.remove('navbar-scrolled');
                }
        })


function submitForm() {
  // Get form data
        var name = document.getElementById("name").value;
        var email = document.getElementById("email").value;
        var message = document.getElementById("message").value;

  // Send form data to server 

  // Show success message
        $("#successModal").modal("show");

  // Clear the form
        document.getElementById("name").value = "";
        document.getElementById("email").value = "";
        document.getElementById("message").value = "";

  // Prevent the form from submitting normally
        return false;
}
