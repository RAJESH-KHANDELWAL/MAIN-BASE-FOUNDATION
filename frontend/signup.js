
"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("signupForm");
  const fullName = document.getElementById("fullName");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");
  const message = document.getElementById("signupMessage");
  const submitButton = document.getElementById("signupSubmit");

  if (
    !form ||
    !fullName ||
    !email ||
    !password ||
    !confirmPassword ||
    !message ||
    !submitButton
  ) {
    console.error("CREATE ACCOUNT form elements are missing.");
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    message.textContent = "";
    message.style.color = "";

    const name = fullName.value.trim();
    const gmail = email.value.trim().toLowerCase();
    const pass = password.value;
    const confirmPass = confirmPassword.value;

    if (!name) {
      message.textContent = "Please enter your FULL NAME.";
      fullName.focus();
      return;
    }

    if (!/^[a-zA-Z0-9._%+-]+@gmail\.com$/i.test(gmail)) {
      message.textContent = "Please enter a valid Gmail ID.";
      email.focus();
      return;
    }

    if (pass.length < 8) {
      message.textContent = "PASSWORD must be at least 8 characters.";
      password.focus();
      return;
    }

    if (pass !== confirmPass) {
      message.textContent = "PASSWORD and CONFIRM PASSWORD do not match.";
      confirmPassword.focus();
      return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "CREATING ACCOUNT...";

    try {
      const response = await fetch("/users/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          full_name: name,
          email: gmail,
          password: pass,
          confirm_password: confirmPass
        })
      });

      const result = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          result.message ||
          result.error ||
          "Account creation failed. Please try again."
        );
      }

      message.style.color = "green";
      message.textContent =
        result.message ||
        "Account created successfully. Please check your email for verification.";

      form.reset();
    } catch (error) {
      message.style.color = "red";
      message.textContent =
        error.message || "Unable to connect to the server.";
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = "CREATE ACCOUNT";
    }
  });
});
