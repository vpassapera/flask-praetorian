function requestRegistration() {
  makeRequest(
    'POST',
    'register',
    {},
    {
      "username": document.getElementById("username").value,
      "email": document.getElementById("email").value,
      "password": document.getElementById("password").value
    }
  );
};

function finalizeRegistration() {
  makeRequest(
    'GET',
    'finalize',
    addTokenHeader(),
  );
};
