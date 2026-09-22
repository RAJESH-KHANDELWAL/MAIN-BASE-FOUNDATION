/* =========================================================
   MAIN BASE FOUNDATION
   LOGIN / AUTHENTICATION
   ========================================================= */

const API_BASE_URL =
    "https://rajeshkhandelwalofficial.onrender.com";


/* =========================================================
   ELEMENTS
   ========================================================= */

const loginForm =
    document.getElementById("loginForm");

const usernameInput =
    document.getElementById("username");

const passwordInput =
    document.getElementById("password");

const loginSubmit =
    document.getElementById("loginSubmit");

const loginMessage =
    document.getElementById("loginMessage");


/* =========================================================
   MESSAGE
   ========================================================= */

function showMessage(
    message,
    type = "error"
) {

    if (!loginMessage) {
        return;
    }

    loginMessage.textContent =
        message;

    loginMessage.dataset.type =
        type;
}


/* =========================================================
   LOGIN
   ========================================================= */

async function login(
    username,
    password
) {

    const response =
        await fetch(
            `${API_BASE_URL}/auth/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "Accept":
                        "application/json"
                },

                body: JSON.stringify({
                    username,
                    password
                })
            }
        );


    const data =
        await response.json()
            .catch(() => ({}));


    if (!response.ok) {

        throw new Error(
            data.detail ||
            data.message ||
            data.error ||
            "LOGIN FAILED"
        );
    }


    return data;
}


/* =========================================================
   SAVE AUTH SESSION
   ========================================================= */

function saveAuthentication(
    data
) {

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
            "LOGIN SUCCEEDED BUT AUTH TOKEN WAS NOT RECEIVED."
        );
    }


    /*
     * Existing backend returns authentication
     * information including token/session data.
     */

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
   FORM SUBMIT
   ========================================================= */

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();


            const username =
                usernameInput.value.trim();

            const password =
                passwordInput.value;


            if (!username) {

                showMessage(
                    "PLEASE ENTER YOUR USERNAME."
                );

                usernameInput.focus();

                return;
            }


            if (!password) {

                showMessage(
                    "PLEASE ENTER YOUR PASSWORD."
                );

                passwordInput.focus();

                return;
            }


            loginSubmit.disabled =
                true;

            loginSubmit.textContent =
                "SIGNING IN...";

            showMessage(
                "CONNECTING TO MAIN BASE FOUNDATION...",
                "loading"
            );


            try {

                const data =
                    await login(
                        username,
                        password
                    );


                saveAuthentication(
                    data
                );


                showMessage(
                    "LOGIN SUCCESSFUL. REDIRECTING...",
                    "success"
                );


                /*
                 * Return to the main application.
                 */

                window.location.href =
                    "index.html";


            } catch (error) {

                console.error(
                    "Login error:",
                    error
                );


                showMessage(
                    error.message ||
                    "LOGIN FAILED. PLEASE TRY AGAIN."
                );


                loginSubmit.disabled =
                    false;

                loginSubmit.textContent =
                    "SIGN IN";
            }

        }
    );
}
