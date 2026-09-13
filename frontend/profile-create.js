/* =========================================================
   MAIN BASE FOUNDATION
   PROFILE CREATION
   ========================================================= */

const API_BASE_URL =
    "https://rajeshkhandelwalofficial.onrender.com";


/* =========================================================
   ELEMENT HELPERS
   ========================================================= */

function getElement(id) {
    return document.getElementById(id);
}


function showMessage(message, type = "info") {

    const element =
        getElement("profileFormMessage");

    if (!element) {
        return;
    }

    element.textContent = message;
    element.dataset.type = type;
}


/* =========================================================
   FORM DATA
   ========================================================= */

function getSelectedProfileType() {

    const selected =
        document.querySelector(
            'input[name="profile_type"]:checked'
        );

    return selected
        ? selected.value
        : "PERSONAL";
}


function getMetadata() {

    const value =
        getElement("metadata").value.trim();

    if (!value) {
        return {};
    }

    try {

        const metadata =
            JSON.parse(value);

        if (
            metadata === null ||
            Array.isArray(metadata) ||
            typeof metadata !== "object"
        ) {

            throw new Error(
                "Metadata must be a JSON object."
            );
        }

        return metadata;

    } catch (error) {

        throw new Error(
            "Profile Metadata must contain valid JSON."
        );
    }
}


/* =========================================================
   CREATE PROFILE REQUEST
   ========================================================= */

async function createProfile(payload) {

    const response =
        await fetch(
            `${API_BASE_URL}/profiles/`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(payload)
            }
        );


    let data = null;

    try {

        data =
            await response.json();

    } catch (error) {

        data = null;
    }


    if (!response.ok) {

        const detail =
            data &&
            data.detail
                ? data.detail
                : `Profile creation failed (${response.status}).`;

        throw new Error(detail);
    }


    return data;
}


/* =========================================================
   FORM SUBMISSION
   ========================================================= */

async function handleProfileSubmit(event) {

    event.preventDefault();

    const form =
        event.currentTarget;

    const submitButton =
        form.querySelector(
            'button[type="submit"]'
        );


    try {

        showMessage(
            "Creating profile...",
            "loading"
        );


        submitButton.disabled = true;


        const payload = {

            profile_id:
                getElement("profileId")
                    .value
                    .trim(),

            master_id:
                getElement("masterId")
                    .value
                    .trim(),

            profile_type:
                getSelectedProfileType(),

            profile_name:
                getElement("profileName")
                    .value
                    .trim(),

            display_name:
                getElement("displayName")
                    .value
                    .trim(),

            description:
                getElement("description")
                    .value
                    .trim(),

            language:
                getElement("language")
                    .value
                    .trim() || "en",

            country:
                getElement("country")
                    .value
                    .trim(),

            state:
                getElement("state")
                    .value
                    .trim(),

            city:
                getElement("city")
                    .value
                    .trim(),

            metadata:
                getMetadata()

        };


        const requiredFields = [
            ["profile_id", "Profile ID"],
            ["master_id", "Master Identity ID"],
            ["profile_name", "Profile Name"]
        ];


        for (
            const [field, label]
            of requiredFields
        ) {

            if (!payload[field]) {

                throw new Error(
                    `${label} is required.`
                );
            }
        }


        const profile =
            await createProfile(payload);


        showMessage(
            "Profile created successfully.",
            "success"
        );


        console.log(
            "Created profile:",
            profile
        );


        setTimeout(
            () => {

                window.location.href =
                    `/profile.html?id=${encodeURIComponent(
                        profile.profile_id
                    )}`;

            },
            800
        );


    } catch (error) {

        console.error(
            "Profile creation error:",
            error
        );


        showMessage(
            error.message ||
                "Unable to create profile.",
            "error"
        );


    } finally {

        submitButton.disabled = false;
    }
}


/* =========================================================
   PROFILE TYPE INTERACTION
   ========================================================= */

function setupProfileTypeSelection() {

    const options =
        document.querySelectorAll(
            'input[name="profile_type"]'
        );


    options.forEach(
        option => {

            option.addEventListener(
                "change",
                () => {

                    options.forEach(
                        item => {

                            const label =
                                item.closest(
                                    ".profile-type-option"
                                );

                            if (!label) {
                                return;
                            }

                            label.dataset.selected =
                                item.checked
                                    ? "true"
                                    : "false";
                        }
                    );

                }
            );

        }
    );
}


/* =========================================================
   INITIALIZE
   ========================================================= */

function initializeProfileCreation() {

    const form =
        getElement("profileCreateForm");


    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        handleProfileSubmit
    );


    setupProfileTypeSelection();

}


/* =========================================================
   START
   ========================================================= */

if (
    document.readyState === "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        initializeProfileCreation
    );

} else {

    initializeProfileCreation();
}
