// Open/Close Modal
const authModal = document.getElementById('auth-modal');
const closeBtn = document.querySelector('.close');
const loginLink = document.querySelector('.login-link');
const authLink = document.getElementById('auth-link');
const usernameDisplayContainer = document.getElementById('username-display-container');
const usernameDisplay = document.getElementById('username-display');

// Open modal when login/register is clicked
loginLink.addEventListener('click', (e) => {
  e.preventDefault();
  authModal.style.display = 'block';
});

// Close modal when close button is clicked
closeBtn.addEventListener('click', () => {
  authModal.style.display = 'none';
});

// Close modal when clicking outside the modal
window.addEventListener('click', (e) => {
  if (e.target === authModal) {
    authModal.style.display = 'none';
  }
});

// Switch between Login and Register forms
const switchToRegister = document.getElementById('switch-to-register');
const switchToLogin = document.getElementById('switch-to-login');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

switchToRegister.addEventListener('click', () => {
  loginForm.style.display = 'none';
  registerForm.style.display = 'block';
});

switchToLogin.addEventListener('click', () => {
  registerForm.style.display = 'none';
  loginForm.style.display = 'block';
});

// Registration and login logic (using localStorage for simplicity)
const usersDB = JSON.parse(localStorage.getItem('users')) || [];

const loginFormSubmit = document.getElementById('login-form-submit');
const registerFormSubmit = document.getElementById('register-form-submit');

// Handle registration form submission
registerFormSubmit.addEventListener('submit', (e) => {
  e.preventDefault();
  const username = document.getElementById('register-username').value;
  const password = document.getElementById('register-password').value;

  if (usersDB.some(user => user.username === username)) {
    alert('Username already exists!');
    return;
  }

  usersDB.push({ username, password });
  localStorage.setItem('users', JSON.stringify(usersDB));
  alert('Registration successful!');
  authModal.style.display = 'none';
});
/*
// Handle login form submission
loginFormSubmit.addEventListener('submit', (e) => {
  e.preventDefault();
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  const user = usersDB.find(user => user.username === username && user.password === password);

  if (user) {
    // Save logged-in user to localStorage
    localStorage.setItem('loggedInUser', JSON.stringify(user));
    alert('Login successful!');
    updateUI();
    authModal.style.display = 'none';
  } else {
    alert('Invalid username or password!');
  }
});
*/
// Update UI to show username and dropdown after login
function updateUI() {
  const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
  if (loggedInUser) {
    authLink.style.display = 'none'; // Hide login/register link
    usernameDisplay.textContent = loggedInUser.username; // Set username display
    usernameDisplayContainer.style.display = 'inline-block'; // Show username and dropdown
  }
}

// Logout logic
const logoutBtn = document.getElementById('logout');
logoutBtn.addEventListener('click', () => {
  localStorage.removeItem('loggedInUser'); // Remove logged-in user from localStorage
  usernameDisplayContainer.style.display = 'none'; // Hide username and dropdown
  authLink.style.display = 'inline-block'; // Show login/register link
  alert('Logged out successfully!');
});

// Run UI update on page load if user is logged in
window.addEventListener('load', updateUI);
