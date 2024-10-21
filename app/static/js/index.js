// Alternar entre formularios de Login y Sign Up
document.getElementById('toggle-form').addEventListener('click', function() {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');

  loginForm.classList.toggle('d-none');
  signupForm.classList.toggle('d-none');

  this.textContent = loginForm.classList.contains('d-none') 
    ? '¿Ya tienes cuenta? Inicia sesión' 
    : '¿No tienes cuenta? Regístrate';
});

// Mostrar/Ocultar contraseña en Login
document.getElementById('toggle-login-password').addEventListener('click', function() {
  const passwordField = document.getElementById('login-password');
  passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
  this.textContent = this.textContent === 'Mostrar' ? 'Ocultar' : 'Mostrar';
});

// Mostrar/Ocultar contraseña en Sign Up (contraseña principal)
document.getElementById('toggle-signup-password').addEventListener('click', function() {
  const passwordField = document.getElementById('signup-password');
  passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
  this.textContent = this.textContent === 'Mostrar' ? 'Ocultar' : 'Mostrar';
});

// Mostrar/Ocultar contraseña en Sign Up (confirmar contraseña)
document.getElementById('toggle-confirm-password').addEventListener('click', function() {
  const confirmPasswordField = document.getElementById('confirm-password');
  confirmPasswordField.type = confirmPasswordField.type === 'password' ? 'text' : 'password';
  this.textContent = this.textContent === 'Mostrar' ? 'Ocultar' : 'Mostrar';
});

// Medidor de fuerza de contraseña
document.getElementById('signup-password').addEventListener('input', function() {
  const strengthMeter = document.getElementById('password-strength');
  const password = this.value;

  let strength = 0;

  // Evaluar la fuerza de la contraseña
  if (password.length >= 8) strength++; // Longitud mínima
  if (/[A-Z]/.test(password)) strength++; // Letra mayúscula
  if (/[a-z]/.test(password)) strength++; // Letra minúscula
  if (/[0-9]/.test(password)) strength++; // Número
  if (/[\W_]/.test(password)) strength++; // Caracter especial

  // Actualizar medidor de fuerza
  strengthMeter.style.display = 'block';
  strengthMeter.className = ''; // Reiniciar clases

  if (strength < 2) {
    strengthMeter.classList.add('weak');
    strengthMeter.textContent = 'Muy débil';
  } else if (strength < 4) {
    strengthMeter.classList.add('medium');
    strengthMeter.textContent = 'Fuerte';
  } else {
    strengthMeter.classList.add('strong');
    strengthMeter.textContent = 'Muy fuerte';
  }
});

// Verificar si las contraseñas coinciden
document.getElementById('signup-form').addEventListener('submit', function(event) {
  const password = document.getElementById('signup-password').value;
  const confirmPassword = document.getElementById('confirm-password').value;

  if (password !== confirmPassword) {
    event.preventDefault();
    alert('Las contraseñas no coinciden');
  }
});
