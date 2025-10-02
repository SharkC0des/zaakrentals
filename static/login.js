// Get the modal
var modal = document.getElementById("login-modal");

// Get the login link and the close button
var loginLink = document.querySelector(".login-link");
var closeBtn = document.querySelector(".close");

// When the user clicks on the "Log in" link, open the modal
loginLink.addEventListener("click", function(event) {
  event.preventDefault(); // Prevent the link from navigating
  modal.style.display = "block"; // Show the modal
});

// When the user clicks on <span> (x), close the modal
closeBtn.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
