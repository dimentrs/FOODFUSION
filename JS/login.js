const authSignUpButton = document.getElementById('authSignUp');
const authSignInButton = document.getElementById('authSignIn');
const authContainer = document.getElementById('authContainer');

authSignUpButton.addEventListener('click', () => {
  authContainer.classList.add("auth-right-active");
});

authSignInButton.addEventListener('click', () => {
  authContainer.classList.remove("auth-right-active");
});