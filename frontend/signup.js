
/* =========================================================
   MAIN BASE FOUNDATION — CREATE ACCOUNT
   SIGNUP + USERNAME HANDOFF TO SIGN IN
   ========================================================= */

const SIGNUP_API =
    "https://rajeshkhandelwalofficial.onrender.com";

const form = document.getElementById("signupForm");
const message = document.getElementById("signupMessage");
const submitButton = document.getElementById("signupSubmit");

function showSignupMessage(text, type = "error") {
    if (!message) return;

    message.textContent = text;
    message.dataset.type = type;
}

if (form) {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const full_name =
            document.getElementById("fullName").value.trim();

        const email =
            document.getElementById("email").value.trim().toLowerCase();

        const password =
            document.getElementById("password").value;

        const confirmPassword =
            document.getElementById("confirmPassword").value;

        if (!full_name) {
            showSignupMessage("PLEASE ENTER YOUR FULL NAME.");
            return;
        }

        if (!/^[a-zA-Z0-9._%+-]+@gmail\.com$/.test(email)) {
            showSignupMessage("PLEASE ENTER A VALID GMAIL ID.");
            return;
        }

        if (password.length < 8) {
            showSignupMessage("PASSWORD MUST BE AT LEAST 8 CHARACTERS.");
            return;
        }

        if (password !== confirmPassword) {
            showSignupMessage("PASSWORDS DO NOT MATCH.");
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "CREATING ACCOUNT...";

        showSignupMessage("CONNECTING TO MAIN BASE FOUNDATION...", "loading");

        try {
            const response = await fetch(
                `${SIGNUP_API}/users/register`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify({
                        full_name,
                        email,
                        password
                    })
                }
            );

            const result = await response.json().catch(() => ({}));

            if (!response.ok) {
                throw new Error(
                    result.detail ||
                    result.message ||
                    "ACCOUNT CREATION FAILED."
                );
            }

            const username =
                result?.data?.username ||
                result?.username ||
                "";

            if (!username) {
                throw new Error(
                    "ACCOUNT CREATED, BUT USERNAME WAS NOT RECEIVED. PLEASE CONTACT SUPPORT."
                );
            }

            // Store only the username for the next sign-in step.
            sessionStorage.setItem(
                "main_base_foundation_pending_username",
                username
            );

            showSignupMessage(
                `ACCOUNT CREATED SUCCESSFULLY!\nYOUR USERNAME: ${username}\nPLEASE USE THIS USERNAME AND YOUR PASSWORD TO SIGN IN.`,
                "success"
            );

            // Add a Sign In link after successful registration.
            let signInLink = document.getElementById("signupSignInLink");

            if (!signInLink) {
                signInLink = document.createElement("a");
                signInLink.id = "signupSignInLink";
                signInLink.href = "login.html";
                signInLink.textContent = "CONTINUE TO SIGN IN";
                signInLink.style.display = "inline-block";
                signInLink.style.marginTop = "16px";
                signInLink.style.fontWeight = "bold";
                message.insertAdjacentElement("afterend", signInLink);
            }

            form.reset();

        } catch (error) {
            showSignupMessage(
                error.message || "UNABLE TO CREATE ACCOUNT. PLEASE TRY AGAIN."
            );
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "CREATE ACCOUNT";
        }
    });
}
