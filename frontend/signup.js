
/* MAIN BASE FOUNDATION — CREATE ACCOUNT */

const SIGNUP_API = "https://rajeshkhandelwalofficial.onrender.com";

const form = document.getElementById("signupForm");
const message = document.getElementById("signupMessage");
const submitButton = document.getElementById("signupSubmit");

function showSignupMessage(text, type = "error") {
  if (!message) return;

  message.textContent = text;
  message.dataset.type = type;
}

form?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const full_name = document
    .getElementById("fullName")
    .value.trim();

  const email = document
    .getElementById("email")
    .value.trim()
    .toLowerCase();

  const password = document
    .getElementById("password")
    .value;

  const confirmPassword = document
    .getElementById("confirmPassword")
    .value;

  // Validate required fields
  if (!full_name) {
    showSignupMessage("PLEASE ENTER YOUR FULL NAME.");
    return;
  }

  if (!email.endsWith("@gmail.com")) {
    showSignupMessage(
      "PLEASE ENTER A VALID GMAIL ID ENDING IN @GMAIL.COM."
    );
    return;
  }

  if (password.length < 8) {
    showSignupMessage(
      "PASSWORD MUST BE AT LEAST 8 CHARACTERS."
    );
    return;
  }

  if (password !== confirmPassword) {
    showSignupMessage(
      "PASSWORD AND CONFIRM PASSWORD DO NOT MATCH."
    );
    return;
  }

  if (submitButton) {
    submitButton.disabled = true;
    submitButton.textContent = "CREATING ACCOUNT...";
  }

  showSignupMessage("");

  try {
    const response = await fetch(
      `${SIGNUP_API}/users/register`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          full_name,
          email,
          password,
        }),
      }
    );

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(
        data.detail ||
          data.message ||
          "ACCOUNT CREATION FAILED."
      );
    }

    const username = data?.data?.username || "";
    const userId = data?.data?.user_id || "";

    showSignupMessage(
      `ACCOUNT CREATED SUCCESSFULLY. USERNAME: ${username}. USER ID: ${userId}. EMAIL VERIFICATION IS NOT CONFIGURED YET.`,
      "success"
    );

    form.reset();
  } catch (error) {
    showSignupMessage(
      error.message ||
        "UNABLE TO CREATE ACCOUNT. PLEASE TRY AGAIN."
    );
  } finally {
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.textContent = "CREATE ACCOUNT";
    }
  }
});
