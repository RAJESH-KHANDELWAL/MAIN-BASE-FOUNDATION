/* =========================================================
   MAIN BASE FOUNDATION
   PLATFORM REVIEW ENGINE
   ========================================================= */

const API_BASE_URL =
    "https://rajeshkhandelwalofficial.onrender.com";


/* =========================================================
   HELPERS
   ========================================================= */

function getElement(id) {
    return document.getElementById(id);
}


function escapeHTML(value) {

    const element =
        document.createElement("div");

    element.textContent =
        value ?? "";

    return element.innerHTML;
}


/* =========================================================
   CHECK DEFINITIONS
   ========================================================= */

const REVIEW_CHECKS = [

    {
        id: "root-api",
        name: "Main API",
        endpoint: "/",
        description:
            "Checks whether the main production API is responding."
    },

    {
        id: "profiles-api",
        name: "Profiles API",
        endpoint: "/profiles/",
        description:
            "Checks whether the universal profile API is responding."
    },

    {
        id: "opportunities-api",
        name: "Opportunities API",
        endpoint: "/opportunities/",
        description:
            "Checks whether the opportunities API is responding."
    },

    {
        id: "live-opportunities",
        name: "Live Opportunities",
        endpoint: "/opportunities/live",
        description:
            "Checks whether live opportunities can be retrieved."
    },

    {
        id: "matching-api",
        name: "Matching API",
        endpoint: "/matching/",
        description:
            "Checks whether the matching API route is available."
    },

    {
        id: "auth-api",
        name: "Authentication API",
        endpoint: "/auth/",
        description:
            "Checks whether the authentication API route is available."
    },

    {
        id: "identity-api",
        name: "Identity API",
        endpoint: "/identity/",
        description:
            "Checks whether the identity API is responding."
    },

    {
        id: "users-api",
        name: "Users API",
        endpoint: "/users/",
        description:
            "Checks whether the users API is responding."
    },

    {
        id: "businesses-api",
        name: "Businesses API",
        endpoint: "/businesses/",
        description:
            "Checks whether the businesses API is responding."
    },

    {
        id: "projects-api",
        name: "Projects API",
        endpoint: "/projects/",
        description:
            "Checks whether the projects API is responding."
    }

];


/* =========================================================
   API CHECK
   ========================================================= */

async function checkEndpoint(check) {

    const startedAt =
        performance.now();

    try {

        const response =
            await fetch(
                `${API_BASE_URL}${check.endpoint}`,
                {
                    method: "GET",
                    headers: {
                        "Accept":
                            "application/json"
                    },
                    cache: "no-store"
                }
            );


        const duration =
            Math.round(
                performance.now() - startedAt
            );


        let body = null;


        try {

            body =
                await response.json();

        } catch (error) {

            body = null;
        }


        return {

            ...check,

            passed:
                response.ok,

            status:
                response.status,

            duration,

            body,

            error:
                response.ok
                    ? null
                    : `HTTP ${response.status}`

        };


    } catch (error) {

        const duration =
            Math.round(
                performance.now() - startedAt
            );


        return {

            ...check,

            passed: false,

            status: 0,

            duration,

            body: null,

            error:
                error.message ||
                "Network request failed."

        };

    }
}


/* =========================================================
   RUN FULL REVIEW
   ========================================================= */

async function runFullReview() {

    const button =
        getElement(
            "runReviewButton"
        );

    const list =
        getElement(
            "reviewList"
        );


    if (!button || !list) {
        return;
    }


    button.disabled = true;

    button.textContent =
        "Running Review...";


    list.innerHTML = `
        <div class="loading-card">
            Checking platform endpoints...
        </div>
    `;


    const results = [];


    for (
        const check
        of REVIEW_CHECKS
    ) {

        const result =
            await checkEndpoint(
                check
            );

        results.push(result);

        renderReviewResults(
            results
        );
    }


    updateSummary(
        results
    );


    const now =
        new Date();


    getElement(
        "reviewTime"
    ).textContent =
        `Last checked: ${now.toLocaleString()}`;


    button.disabled = false;

    button.textContent =
        "Run Full Review";
}


/* =========================================================
   RENDER RESULTS
   ========================================================= */

function renderReviewResults(
    results
) {

    const list =
        getElement(
            "reviewList"
        );


    if (!list) {
        return;
    }


    list.innerHTML =
        results
            .map(
                result => {

                    const state =
                        result.passed
                            ? "PASS"
                            : "FAIL";


                    const stateClass =
                        result.passed
                            ? "review-pass"
                            : "review-fail";


                    const statusText =
                        result.status
                            ? `HTTP ${result.status}`
                            : "NO RESPONSE";


                    const responseBody =
                        result.body
                            ? escapeHTML(
                                JSON.stringify(
                                    result.body
                                )
                            )
                            : "";


                    return `
                        <article
                            class="review-item ${stateClass}"
                        >

                            <div class="review-item-main">

                                <div class="review-status">
                                    ${state}
                                </div>

                                <div>

                                    <h3>
                                        ${escapeHTML(
                                            result.name
                                        )}
                                    </h3>

                                    <p>
                                        ${escapeHTML(
                                            result.description
                                        )}
                                    </p>

                                </div>

                            </div>


                            <div class="review-item-meta">

                                <span>
                                    ${escapeHTML(
                                        result.endpoint
                                    )}
                                </span>

                                <span>
                                    ${statusText}
                                </span>

                                <span>
                                    ${result.duration} ms
                                </span>

                            </div>


                            ${
                                result.error
                                    ? `
                                        <div class="review-error">
                                            ${escapeHTML(
                                                result.error
                                            )}
                                        </div>
                                    `
                                    : ""
                            }


                            ${
                                responseBody
                                    ? `
                                        <details
                                            class="review-response"
                                        >

                                            <summary>
                                                Response
                                            </summary>

                                            <pre>${responseBody}</pre>

                                        </details>
                                    `
                                    : ""
                            }

                        </article>
                    `;
                }
            )
            .join("");
}


/* =========================================================
   SUMMARY
   ========================================================= */

function updateSummary(
    results
) {

    const passed =
        results.filter(
            result =>
                result.passed
        ).length;


    const failed =
        results.filter(
            result =>
                !result.passed
        ).length;


    getElement(
        "reviewPassed"
    ).textContent =
        passed;


    getElement(
        "reviewFailed"
    ).textContent =
        failed;


    getElement(
        "reviewTotal"
    ).textContent =
        results.length;
}


/* =========================================================
   INITIALIZE
   ========================================================= */

function initializeReview() {

    const button =
        getElement(
            "runReviewButton"
        );


    if (!button) {
        return;
    }


    button.addEventListener(
        "click",
        runFullReview
    );


    runFullReview();
}


/* =========================================================
   START
   ========================================================= */

if (
    document.readyState === "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        initializeReview
    );

} else {

    initializeReview();
}
