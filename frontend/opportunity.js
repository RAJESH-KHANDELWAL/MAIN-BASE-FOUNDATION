/* =========================================================
   MAIN BASE FOUNDATION
   OPPORTUNITY DETAIL PAGE
   API CONNECTION
   ========================================================= */

const API_BASE_URL =
    "https://rajeshkhandelwalofficial.onrender.com";


/* =========================================================
   HELPERS
   ========================================================= */

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


/* =========================================================
   OPPORTUNITY ID
   ========================================================= */

function getOpportunityId() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    return params.get("id");
}


/* =========================================================
   ERROR
   ========================================================= */

function showError(message) {

    const loading =
        getElement(
            "opportunityLoading"
        );

    const error =
        getElement(
            "opportunityError"
        );

    if (loading) {
        loading.hidden = true;
    }

    if (error) {

        error.hidden = false;

        error.textContent =
            message;
    }
}


/* =========================================================
   FORMAT LIST
   ========================================================= */

function formatList(value) {

    if (Array.isArray(value)) {

        return value.length
            ? value.join(", ")
            : "—";
    }

    return value || "—";
}


/* =========================================================
   FORMAT BUDGET
   ========================================================= */

function formatBudget(
    opportunity
) {

    if (
        opportunity.budget === null ||
        opportunity.budget === undefined ||
        opportunity.budget === ""
    ) {

        return "—";
    }

    const currency =
        opportunity.currency || "";

    return `${currency} ${opportunity.budget}`
        .trim();
}


/* =========================================================
   SHOW OPPORTUNITY
   ========================================================= */

function showOpportunity(
    opportunity
) {

    const loading =
        getElement(
            "opportunityLoading"
        );

    const card =
        getElement(
            "opportunityCard"
        );

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
        `Owner: ${
            opportunity.owner_id || "—"
        }`
    );


    setText(
        "opportunityId",
        opportunity.opportunity_id
    );


    setText(
        "opportunitySkills",
        formatList(
            opportunity.skills
        )
    );


    setText(
        "opportunityLanguages",
        formatList(
            opportunity.languages
        )
    );


    setText(
        "opportunityBudget",
        formatBudget(
            opportunity
        )
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


/* =========================================================
   LOAD OPPORTUNITY
   ========================================================= */

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
                `${API_BASE_URL}/opportunities/${encodeURIComponent(
                    opportunityId
                )}`
            );


        if (!response.ok) {

            throw new Error(
                `Opportunity request failed with HTTP ${response.status}.`
            );
        }


        const responseData =
            await response.json();


        /*
         * Backend may return:
         *
         * {
         *     opportunity_id: "...",
         *     ...
         * }
         *
         * OR:
         *
         * {
         *     message: "...",
         *     data: {
         *         opportunity_id: "...",
         *         ...
         *     }
         * }
         */

        const opportunity =
            responseData?.data &&
            typeof responseData.data === "object"
                ? responseData.data
                : responseData;


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


/* =========================================================
   START
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    loadOpportunity
);
