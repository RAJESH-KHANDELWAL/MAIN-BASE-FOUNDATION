
/* =========================================================
   MAIN BASE FOUNDATION — SIGN IN
   AUTHENTICATION SYSTEM
   ========================================================= */

const SIGN_IN_API =
    "https://rajeshkhandelwalofficial.onrender.com";

const signInForm =
    document.getElementById("signInForm");

const usernameInput =
    document.getElementById("signInUsername");

const passwordInput =
    document.getElementById("signInPassword");

const submitButton =
    document.getElementById("signInSubmit");

const message =
    document.getElementById("signInMessage");

/* =========================================================
   MESSAGE HANDLER
   ========================================================= */

function showSignInMessage(text, type = "error") {
    message.textContent = text;
    message.dataset.type = type;
}

/* =========================================================
   SIGNUP → SIGN IN USERNAME AUTOFILL
   ========================================================= */

(function prefillUsername() {
    const pendingUsername = sessionStorage.getItem(
        "main_base_foundation_pending_username"
    );

    if (pendingUsername) {
        usernameInput.value = pendingUsername;

        sessionStorage.removeItem(
            "main_base_foundation_pending_username"
        );
    }
})();

/* =========================================================
   AUTHENTICATION API
   ========================================================= */

async function authenticateSignIn(username, password) {
    const response = await fetch(
        `${SIGN_IN_API}/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        }
    );

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(
            data.detail ||
            data.message ||
            data.error ||
            "SIGN IN FAILED. PLEASE CHECK YOUR USERNAME AND PASSWORD."
        );
    }

    return data;
}

/* =========================================================
   SAVE AUTHENTICATION SESSION
   ========================================================= */

function saveSignInSession(data) {
    const token =
        data?.token ||
        data?.access_token ||
        "";

    const sessionId =
        data?.session_id ||
        "";

    const userId =
        data?.user_id ||
        data?.id ||
        data?.identity_id ||
        "";

    if (!token) {
        throw new Error(
            "AUTHENTICATION TOKEN WAS NOT RECEIVED."
        );
    }

    sessionStorage.setItem(
        "main_base_foundation_token",
        token
    );

    if (sessionId) {
        sessionStorage.setItem(
            "main_base_foundation_session_id",
            sessionId
        );
    }

    if (userId) {
        sessionStorage.setItem(
            "main_base_foundation_user_id",
            userId
        );
    }

    sessionStorage.setItem(
        "main_base_foundation_authenticated",
        "true"
    );
}

/* =========================================================
   SIGN IN FORM SUBMISSION
   ========================================================= */

signInForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    if (!username) {
        showSignInMessage("PLEASE ENTER YOUR USERNAME.");
        usernameInput.focus();
        return;
    }

    if (!password) {
        showSignInMessage("PLEASE ENTER YOUR PASSWORD.");
        passwordInput.focus();
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "SIGNING IN...";

    showSignInMessage(
        "CONNECTING TO MAIN BASE FOUNDATION...",
        "loading"
    );

    try {
        const data = await authenticateSignIn(
            username,
            password
        );

        saveSignInSession(data);

        showSignInMessage(
            "SIGN IN SUCCESSFUL. REDIRECTING...",
            "success"
        );

        window.location.href = "index.html";

    } catch (error) {
        console.error("Sign In Error:", error);

        showSignInMessage(
            error.message ||
            "SIGN IN FAILED. PLEASE TRY AGAIN."
        );

        submitButton.disabled = false;
        submitButton.textContent = "SIGN IN";
    }
});
