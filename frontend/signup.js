
"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signupForm");
  const fullNameInput = document.getElementById("fullName");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirmPassword");
  const submitButton = document.getElementById("signupSubmit");
  const messageBox = document.getElementById("signupMessage");

  if (
    !signupForm ||
    !fullNameInput ||
    !emailInput ||
    !passwordInput ||
    !confirmPasswordInput ||
    !submitButton ||
    !messageBox
  ) {
    console.error("Signup form elements are missing.");
    return;
  }

  // API endpoint: same-origin backend route.
  const REGISTER_API_URL = "/users/register";

  function showMessage(message, type = "error") {
    messageBox.textContent = message;
    messageBox.style.color =
      type === "success" ? "#15803d" : "#b91c1c";
  }

  function setLoading(isLoading) {
    submitButton.disabled = isLoading;
    submitButton.textContent = isLoading
      ? "CREATING ACCOUNT..."
      : "CREATE ACCOUNT";
  }

  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const fullName = fullNameInput.value.trim();
    const email = emailInput.value.trim().toLowerCase();
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    messageBox.textContent = "";

    if (!fullName) {
      showMessage("Please enter your full name.");
      fullNameInput.focus();
      return;
    }

    if (!/^[^\s@]+@gmail\.com$/i.test(email)) {
      showMessage("Please enter a valid Gmail address ending in @gmail.com.");
      emailInput.focus();
      return;
    }

    if (password.length < 8) {
      showMessage("Password must contain at least 8 characters.");
      passwordInput.focus();
      return;
    }

    if (password !== confirmPassword) {
      showMessage("Passwords do not match.");
      confirmPasswordInput.focus();
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(REGISTER_API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        credentials: "same-origin",
        body: JSON.stringify({
          full_name: fullName,
          email: email,
          password: password
        })
      });

      let result = {};

      try {
        result = await response.json();
      } catch {
        result = {};
      }

      if (!response.ok) {
        const errorMessage =
          result.detail ||
          result.message ||
          result.error ||
          "Account creation failed. Please try again.";

        showMessage(
          typeof errorMessage === "string"
            ? errorMessage
            : "Please check your information and try again."
        );
        return;
      }

      showMessage(
        result.message ||
          "Account created successfully. You can now sign in.",
        "success"
      );

      signupForm.reset();

      // Redirect to the existing sign-in page.
      window.setTimeout(() => {
        window.location.href = "login.html";
      }, 1500);

    } catch (error) {
      console.error("Signup request failed:", error);

      showMessage(
        "Unable to connect to the server. Please check your connection and try again."
      );
    } finally {
      setLoading(false);
    }
  });
});
