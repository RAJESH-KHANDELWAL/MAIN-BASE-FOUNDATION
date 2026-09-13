/* =========================================================
   MAIN BASE FOUNDATION
   PUBLIC WEB APPLICATION
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
    const element = getElement(id);

    if (element) {
        element.textContent = value;
    }
}


function escapeHTML(value) {
    const element = document.createElement("div");

    element.textContent = value ?? "";

    return element.innerHTML;
}


/* =========================================================
   API REQUEST
   ========================================================= */

async function apiRequest(path, options = {}) {

    const response = await fetch(
        `${API_BASE_URL}${path}`,
        {
            ...options,

            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            }
        }
    );

    if (!response.ok) {
        throw new Error(
            `API request failed: ${response.status}`
        );
    }

    return response.json();
}


/* =========================================================
   API STATUS
   ========================================================= */

async function checkAPIStatus() {

    const statusElement = getElement("apiStatus");

    if (!statusElement) {
        return;
    }

    try {

        const data = await apiRequest("/");

        if (
            data &&
            data.status === "RUNNING"
        ) {

            statusElement.textContent =
                "API connected";

        } else {

            statusElement.textContent =
                "API available";
        }

    } catch (error) {

        console.error(
            "API status error:",
            error
        );

        statusElement.textContent =
            "API unavailable";
    }
}


/* =========================================================
   LOAD PROFILES
   ========================================================= */

async function loadProfiles() {

    try {

        const profiles =
            await apiRequest("/profiles/");

        if (Array.isArray(profiles)) {

            setText(
                "profileCount",
                profiles.length
            );

            return profiles;
        }

        setText(
            "profileCount",
            0
        );

        return [];

    } catch (error) {

        console.error(
            "Profile loading error:",
            error
        );

        setText(
            "profileCount",
            "—"
        );

        return [];
    }
}


/* =========================================================
   LOAD LIVE OPPORTUNITIES
   ========================================================= */

async function loadOpportunities() {

    const container =
        getElement("opportunityList");

    if (!container) {
        return;
    }

    try {

        const opportunities =
            await apiRequest(
                "/opportunities/live"
            );

        if (
            !Array.isArray(opportunities) ||
            opportunities.length === 0
        ) {

            setText(
                "opportunityCount",
                0
            );

            container.innerHTML = `
                <div class="loading-card">
                    No live opportunities available yet.
                </div>
            `;

            return [];
        }


        setText(
            "opportunityCount",
            opportunities.length
        );


        container.innerHTML =
            opportunities
                .map(
                    opportunity =>
                        createOpportunityCard(
                            opportunity
                        )
                )
                .join("");


        return opportunities;

    } catch (error) {

        console.error(
            "Opportunity loading error:",
            error
        );

        setText(
            "opportunityCount",
            "—"
        );

        container.innerHTML = `
            <div class="loading-card">
                Live opportunities could not be loaded.
            </div>
        `;

        return [];
    }
}


/* =========================================================
   OPPORTUNITY CARD
   ========================================================= */

function createOpportunityCard(
    opportunity
) {

    const title =
        escapeHTML(
            opportunity.title ||
            "Untitled Opportunity"
        );

    const description =
        escapeHTML(
            opportunity.description ||
            "No description available."
        );

    const type =
        escapeHTML(
            opportunity.opportunity_type ||
            "Opportunity"
        );

    const budget =
        Number(
            opportunity.budget || 0
        );

    const currency =
        escapeHTML(
            opportunity.currency ||
            "INR"
        );

    const skills =
        Array.isArray(
            opportunity.skills
        )
            ? opportunity.skills
            : [];


    const skillTags =
        skills
            .slice(0, 6)
            .map(
                skill => `
                    <span class="opportunity-tag">
                        ${escapeHTML(skill)}
                    </span>
                `
            )
            .join("");


    return `
        <article class="opportunity-card">

            <div class="eyebrow">
                ${type}
            </div>

            <h3>
                ${title}
            </h3>

            <p>
                ${description}
            </p>

            <div class="opportunity-meta">

                <span class="opportunity-tag">
                    ${currency} ${budget.toLocaleString("en-IN")}
                </span>

                ${skillTags}

            </div>

        </article>
    `;
}


/* =========================================================
   LOGIN BUTTON
   ========================================================= */

function setupLoginButton() {

    const button =
        getElement("loginButton");

    if (!button) {
        return;
    }

    button.addEventListener(
        "click",
        () => {

            window.location.href =
                "/login.html";

        }
    );
}


/* =========================================================
   INITIALIZE APPLICATION
   ========================================================= */

async function initializeApplication() {

    await checkAPIStatus();

    await Promise.all([
        loadProfiles(),
        loadOpportunities()
    ]);

    setupLoginButton();
}


/* =========================================================
   START
   ========================================================= */

if (
    document.readyState === "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        initializeApplication
    );

} else {

    initializeApplication();
}
