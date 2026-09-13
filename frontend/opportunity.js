const API_BASE_URL =
    "https://rajeshkhandelwalofficial.onrender.com";


function getElement(id) {
    return document.getElementById(id);
}


function setText(id, value) {

    const element =
        getElement(id);

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


function getOpportunityId() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    return params.get("id");
}


function showError(message) {

    const loading =
        getElement("opportunityLoading");

    const error =
        getElement("opportunityError");

    if (loading) {
        loading.hidden = true;
    }

    if (error) {
        error.hidden = false;
        error.textContent = message;
    }
}


function formatList(value) {

    if (Array.isArray(value)) {
        return value.length
            ? value.join(", ")
            : "—";
    }

    return value || "—";
}


function formatBudget(opportunity) {

    if (
        opportunity.budget === null ||
        opportunity.budget === undefined ||
        opportunity.budget === ""
    ) {
        return "—";
    }

    const currency =
        opportunity.currency || "";

    return `${currency} ${opportunity.budget}`.trim();
}


function showOpportunity(opportunity) {

    const loading =
        getElement("opportunityLoading");

    const card =
        getElement("opportunityCard");

    if (loading) {
        loading.hidden = true;
    }

    if (card) {
        card.hidden = false;
    }


    setText(
        "opportunityType",
        opportunity.opportunity_type
    );

    setText(
        "opportunityTitle",
        opportunity.title
    );

    setText(
        "opportunityOwner",
        `Owner: ${opportunity.owner_id || "—"}`
    );

    setText(
        "opportunityId",
        opportunity.opportunity_id
    );

    setText(
        "opportunitySkills",
        formatList(opportunity.skills)
    );

    setText(
        "opportunityLanguages",
        formatList(opportunity.languages)
    );

    setText(
        "opportunityBudget",
        formatBudget(opportunity)
    );

    setText(
        "opportunityDeadline",
        opportunity.deadline
    );

    setText(
        "opportunityAvailability",
        opportunity.availability
    );

    setText(
        "opportunityDescription",
        opportunity.description
    );

    setText(
        "opportunityStatus",
        opportunity.status
    );
}


async function loadOpportunity() {

    const opportunityId =
        getOpportunityId();

    if (!opportunityId) {

        showError(
            "No opportunity ID was provided."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/opportunities/${encodeURIComponent(opportunityId)}`
            );


        if (!response.ok) {

            throw new Error(
                `Opportunity request failed with HTTP ${response.status}.`
            );
        }


        const opportunity =
            await response.json();


        if (
            !opportunity ||
            !opportunity.opportunity_id
        ) {

            throw new Error(
                "The API returned an invalid opportunity."
            );
        }


        showOpportunity(
            opportunity
        );

    } catch (error) {

        console.error(
            "Opportunity loading error:",
            error
        );

        showError(
            error.message ||
            "Unable to load this opportunity."
        );
    }
}


document.addEventListener(
    "DOMContentLoaded",
    loadOpportunity
);
