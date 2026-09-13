const API_BASE_URL =
    "https://rajeshkhandelwalofficial.onrender.com";


function getElement(id) {
    return document.getElementById(id);
}


function setText(id, value) {
    const element = getElement(id);

    if (!element) {
        return;
    }

    element.textContent =
        value === null ||
        value === undefined ||
        value === ""
            ? "—"
            : String(value);
}


function getProfileId() {
    const params =
        new URLSearchParams(window.location.search);

    return params.get("id");
}


function getLocation(profile) {
    const parts = [
        profile.country,
        profile.state,
        profile.city,
    ].filter(Boolean);

    return parts.length
        ? parts.join(", ")
        : "—";
}


function showError(message) {
    const loading =
        getElement("profileLoading");

    const error =
        getElement("profileError");

    if (loading) {
        loading.hidden = true;
    }

    if (error) {
        error.hidden = false;
        error.textContent = message;
    }
}


function showProfile(profile) {

    const loading =
        getElement("profileLoading");

    const card =
        getElement("profileCard");

    if (loading) {
        loading.hidden = true;
    }

    if (card) {
        card.hidden = false;
    }


    setText(
        "profileType",
        profile.profile_type
    );

    setText(
        "profileName",
        profile.profile_name
    );

    setText(
        "profileDisplayName",
        profile.display_name
    );

    setText(
        "profileId",
        profile.profile_id
    );

    setText(
        "masterId",
        profile.master_id
    );

    setText(
        "profileLocation",
        getLocation(profile)
    );

    setText(
        "profileLanguage",
        profile.language
    );

    setText(
        "profileStatus",
        profile.status
    );

    setText(
        "profileDescription",
        profile.description
    );


    const verified =
        getElement("profileVerified");

    if (verified) {

        verified.textContent =
            profile.verified
                ? "VERIFIED"
                : "NOT VERIFIED";

        verified.className =
            profile.verified
                ? "review-status review-pass"
                : "review-status";
    }


    const metadata =
        getElement("profileMetadata");

    if (metadata) {

        metadata.textContent =
            JSON.stringify(
                profile.metadata || {},
                null,
                2
            );
    }
}


async function loadProfile() {

    const profileId =
        getProfileId();

    if (!profileId) {

        showError(
            "No profile ID was provided."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/profiles/${encodeURIComponent(profileId)}`
            );


        if (!response.ok) {

            throw new Error(
                `Profile request failed with HTTP ${response.status}.`
            );
        }


        const profile =
            await response.json();


        if (!profile || !profile.profile_id) {

            throw new Error(
                "The API returned an invalid profile."
            );
        }


        showProfile(profile);

    } catch (error) {

        console.error(
            "Profile loading error:",
            error
        );

        showError(
            error.message ||
            "Unable to load this profile."
        );
    }
}


document.addEventListener(
    "DOMContentLoaded",
    loadProfile
);
