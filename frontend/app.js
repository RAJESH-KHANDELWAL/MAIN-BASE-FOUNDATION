/* =========================================================
   MAIN BASE FOUNDATION
   REAL WEB APPLICATION
   AUTHENTICATION + PROJECT WORKSPACE + API
   ========================================================= */


/* =========================================================
   API CONFIGURATION
   ========================================================= */

const API_BASE_URL =
    "https://api.rajeshkhandelwalofficial.com";


/* =========================================================
   STORAGE KEYS
   ========================================================= */

const TOKEN_KEY =
    "main_base_foundation_token";

const SESSION_ID_KEY =
    "main_base_foundation_session_id";

const USER_ID_KEY =
    "main_base_foundation_user_id";

const AUTHENTICATED_KEY =
    "main_base_foundation_authenticated";


/* =========================================================
   HELPERS
   ========================================================= */

function getElement(id) {

    return document.getElementById(id);
}


function setText(id, value) {

    const element =
        getElement(id);

    if (element) {

        element.textContent =
            value ?? "";

    }
}


function escapeHTML(value) {

    const element =
        document.createElement("div");

    element.textContent =
        value ?? "";

    return element.innerHTML;
}


/* =========================================================
   AUTHENTICATION HELPERS
   ========================================================= */

function getAuthToken() {

    return sessionStorage.getItem(
        TOKEN_KEY
    ) || "";
}


function getSessionId() {

    return sessionStorage.getItem(
        SESSION_ID_KEY
    ) || "";
}


function getStoredUserId() {

    return sessionStorage.getItem(
        USER_ID_KEY
    ) || "";
}


function isAuthenticated() {

    return Boolean(
        getAuthToken()
    );

}


/* =========================================================
   AUTHENTICATED API REQUEST
   ========================================================= */

async function apiRequest(
    path,
    options = {}
) {

    const token =
        getAuthToken();

    const headers = {

        "Content-Type":
            "application/json",

        "Accept":
            "application/json",

        ...(options.headers || {})

    };


    if (token) {

        headers.Authorization =
            `Bearer ${token}`;

    }


    const response =
        await fetch(
            `${API_BASE_URL}${path}`,
            {
                ...options,
                headers
            }
        );


    const data =
        await response
            .json()
            .catch(
                () => ({})
            );


    if (
        response.status === 401
    ) {

        handleAuthenticationExpired();

        throw new Error(
            "AUTHENTICATION SESSION EXPIRED."
        );

    }


    if (!response.ok) {

        throw new Error(

            data?.detail ||
            data?.message ||
            data?.error ||
            `API REQUEST FAILED: ${response.status}`

        );

    }


    return data;
}


/* =========================================================
   PUBLIC API REQUEST
   ========================================================= */

async function publicApiRequest(
    path,
    options = {}
) {

    const response =
        await fetch(
            `${API_BASE_URL}${path}`,
            {
                ...options,

                headers: {

                    "Content-Type":
                        "application/json",

                    "Accept":
                        "application/json",

                    ...(options.headers || {})

                }

            }
        );


    const data =
        await response
            .json()
            .catch(
                () => ({})
            );


    if (!response.ok) {

        throw new Error(

            data?.detail ||
            data?.message ||
            data?.error ||
            `API REQUEST FAILED: ${response.status}`

        );

    }


    return data;
}


/* =========================================================
   AUTHENTICATION SESSION UI
   ========================================================= */

function showAuthenticatedWorkspace() {

    const workspace =
        getElement(
            "projectWorkspace"
        );

    if (workspace) {

        workspace.classList.add(
            "is-visible"
        );

    }


    const loginButton =
        getElement(
            "loginButton"
        );

    if (loginButton) {

        loginButton.textContent =
            "WORKSPACE";

        loginButton.onclick =
            () => {

                const target =
                    getElement(
                        "projectWorkspace"
                    );

                if (target) {

                    target.scrollIntoView({
                        behavior: "smooth"
                    });

                }

            };

    }

}


function hideAuthenticatedWorkspace() {

    const workspace =
        getElement(
            "projectWorkspace"
        );

    if (workspace) {

        workspace.classList.remove(
            "is-visible"
        );

    }


    const loginButton =
        getElement(
            "loginButton"
        );

    if (loginButton) {

        loginButton.textContent =
            "SIGN IN";

        loginButton.onclick =
            () => {

                window.location.href =
                    "/login.html";

            };

    }

}


/* =========================================================
   AUTHENTICATION VALIDATION
   ========================================================= */

async function validateAuthentication() {

    const token =
        getAuthToken();


    if (!token) {

        hideAuthenticatedWorkspace();

        return false;

    }


    try {

        const response =
            await publicApiRequest(
                "/auth/validate",
                {
                    method: "POST",

                    body: JSON.stringify({
                        token
                    })
                }
            );


        if (
            response &&
            response.authenticated === true
        ) {

            showAuthenticatedWorkspace();


            const username =
                response.username ||
                "AUTHENTICATED USER";


            setText(
                "workspaceUser",
                `SIGNED IN AS: ${username}`
            );


            if (
                response.identity_id &&
                !getStoredUserId()
            ) {

                sessionStorage.setItem(
                    USER_ID_KEY,
                    response.identity_id
                );

            }


            return true;

        }


        handleAuthenticationExpired();

        return false;


    } catch (error) {

        console.error(
            "Authentication validation error:",
            error
        );

        hideAuthenticatedWorkspace();

        return false;

    }

}


/* =========================================================
   AUTHENTICATION EXPIRED
   ========================================================= */

function handleAuthenticationExpired() {

    sessionStorage.removeItem(
        TOKEN_KEY
    );

    sessionStorage.removeItem(
        SESSION_ID_KEY
    );

    sessionStorage.removeItem(
        USER_ID_KEY
    );

    sessionStorage.removeItem(
        AUTHENTICATED_KEY
    );


    hideAuthenticatedWorkspace();

}


/* =========================================================
   API STATUS
   ========================================================= */

async function checkAPIStatus() {

    const statusElement =
        getElement(
            "apiStatus"
        );


    if (!statusElement) {

        return;

    }


    try {

        const data =
            await publicApiRequest(
                "/"
            );


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

        const response =
            await publicApiRequest(
                "/profiles/"
            );


        const profiles =
            Array.isArray(response)
                ? response
                : Array.isArray(
                    response?.data
                )
                    ? response.data
                    : [];


        setText(
            "profileCount",
            profiles.length
        );


        return profiles;


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
        getElement(
            "opportunityList"
        );


    if (!container) {

        return [];

    }


    try {

        const response =
            await publicApiRequest(
                "/opportunities/live"
            );


        const opportunities =
            Array.isArray(response)
                ? response
                : Array.isArray(
                    response?.data
                )
                    ? response.data
                    : [];


        if (
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
                    ${currency}
                    ${budget.toLocaleString("en-IN")}
                </span>

                ${skillTags}

            </div>

        </article>
    `;

}


/* =========================================================
   WORKSPACE MESSAGE
   ========================================================= */

function showWorkspaceMessage(
    message,
    type = ""
) {

    const element =
        getElement(
            "workspaceMessage"
        );


    if (!element) {

        return;

    }


    element.textContent =
        message || "";


    element.className =
        "workspace-message";


    if (type) {

        element.classList.add(
            type
        );

    }

}


/* =========================================================
   LOAD PROJECTS
   ========================================================= */

async function loadProjects() {

    const container =
        getElement(
            "projectList"
        );


    if (!container) {

        return [];

    }


    container.innerHTML = `
        <div class="project-loading">
            Loading your projects...
        </div>
    `;


    try {

        const userId =
            getStoredUserId();


        let path =
            "/projects/";


        /*
         * Existing backend requires owner_id
         * for project creation.
         *
         * If identity_id is available,
         * use it to filter projects.
         */

        if (userId) {

            path +=
                `?owner_id=${encodeURIComponent(
                    userId
                )}`;

        }


        const response =
            await apiRequest(
                path
            );


        const projects =
            Array.isArray(response)
                ? response
                : Array.isArray(
                    response?.data
                )
                    ? response.data
                    : [];


        updateProjectStatistics(
            projects
        );


        if (
            projects.length === 0
        ) {

            container.innerHTML = `
                <div class="project-empty">
                    <h3>
                        NO PROJECTS YET
                    </h3>

                    <p>
                        Create your first real project
                        using the button above.
                    </p>
                </div>
            `;

            return [];

        }


        container.innerHTML =
            projects
                .map(
                    project =>
                        createProjectCard(
                            project
                        )
                )
                .join("");


        return projects;


    } catch (error) {

        console.error(
            "Project loading error:",
            error
        );


        container.innerHTML = `
            <div class="project-error">
                ${escapeHTML(
                    error.message ||
                    "PROJECTS COULD NOT BE LOADED."
                )}
            </div>
        `;


        return [];

    }

}


/* =========================================================
   PROJECT STATISTICS
   ========================================================= */

function updateProjectStatistics(
    projects
) {

    const total =
        projects.length;


    const active =
        projects.filter(
            project =>
                String(
                    project.status || ""
                ).toUpperCase() ===
                "ACTIVE"
        ).length;


    const completed =
        projects.filter(
            project =>
                String(
                    project.status || ""
                ).toUpperCase() ===
                "COMPLETED"
        ).length;


    setText(
        "totalProjects",
        total
    );


    setText(
        "activeProjects",
        active
    );


    setText(
        "completedProjects",
        completed
    );

}


/* =========================================================
   PROJECT CARD
   ========================================================= */

function createProjectCard(
    project
) {

    const id =
        escapeHTML(
            project.project_id || ""
        );


    const name =
        escapeHTML(
            project.name ||
            "Untitled Project"
        );


    const description =
        escapeHTML(
            project.description ||
            "No description available."
        );


    const projectType =
        escapeHTML(
            project.project_type ||
            "GENERAL"
        );


    const status =
        escapeHTML(
            project.status ||
            "ACTIVE"
        );


    const visibility =
        escapeHTML(
            project.visibility ||
            "PRIVATE"
        );


    const currency =
        escapeHTML(
            project.currency ||
            "INR"
        );


    const budget =
        Number(
            project.budget || 0
        );


    const deadline =
        escapeHTML(
            project.deadline ||
            "No deadline"
        );


    return `
        <article
            class="project-card"
            data-project-id="${id}"
        >

            <div class="project-card-header">

                <div>

                    <h3>
                        ${name}
                    </h3>

                    <span class="project-status">
                        ${status}
                    </span>

                </div>

            </div>


            <p class="project-description">
                ${description}
            </p>


            <div class="project-meta">

                <span>
                    TYPE: ${projectType}
                </span>

                <span>
                    VISIBILITY: ${visibility}
                </span>

                <span>
                    BUDGET:
                    ${currency}
                    ${budget.toLocaleString("en-IN")}
                </span>

                <span>
                    DEADLINE:
                    ${deadline}
                </span>

            </div>


            <div class="project-actions">

                <button
                    type="button"
                    onclick="changeProjectStatus(
                        '${id}',
                        'ACTIVE'
                    )"
                >
                    ACTIVE
                </button>


                <button
                    type="button"
                    onclick="changeProjectStatus(
                        '${id}',
                        'ON_HOLD'
                    )"
                >
                    ON HOLD
                </button>


                <button
                    type="button"
                    onclick="changeProjectStatus(
                        '${id}',
                        'COMPLETED'
                    )"
                >
                    COMPLETED
                </button>


                <button
                    type="button"
                    onclick="deleteProject(
                        '${id}'
                    )"
                >
                    DELETE
                </button>

            </div>

        </article>
    `;

}


/* =========================================================
   CREATE PROJECT
   ========================================================= */

async function createProject(
    event
) {

    event.preventDefault();


    const ownerId =
        getStoredUserId();


    if (!ownerId) {

        showWorkspaceMessage(
            "AUTHENTICATED USER ID WAS NOT FOUND.",
            "error"
        );

        return;

    }


    const name =
        getElement(
            "projectName"
        )?.value.trim();


    const description =
        getElement(
            "projectDescription"
        )?.value.trim() ||
        "";


    const projectType =
        getElement(
            "projectType"
        )?.value.trim() ||
        "GENERAL";


    const status =
        getElement(
            "projectStatus"
        )?.value ||
        "ACTIVE";


    const visibility =
        getElement(
            "projectVisibility"
        )?.value ||
        "PRIVATE";


    const budgetValue =
        getElement(
            "projectBudget"
        )?.value;


    const budget =
        budgetValue === ""
            ? null
            : Number(
                budgetValue
            );


    const currency =
        getElement(
            "projectCurrency"
        )?.value.trim() ||
        "INR";


    const deadline =
        getElement(
            "projectDeadline"
        )?.value ||
        null;


    if (!name) {

        showWorkspaceMessage(
            "PROJECT NAME IS REQUIRED.",
            "error"
        );

        return;

    }


    const submitButton =
        document.querySelector(
            "#projectForm button[type='submit']"
        );


    if (submitButton) {

        submitButton.disabled =
            true;

        submitButton.textContent =
            "SAVING...";

    }


    try {

        await apiRequest(
            "/projects/",
            {
                method: "POST",

                body: JSON.stringify({

                    owner_id:
                        ownerId,

                    name:
                        name,

                    description:
                        description,

                    project_type:
                        projectType,

                    status:
                        status,

                    visibility:
                        visibility,

                    budget:
                        budget,

                    currency:
                        currency,

                    deadline:
                        deadline

                })

            }
        );


        showWorkspaceMessage(
            "PROJECT CREATED SUCCESSFULLY.",
            "success"
        );


        resetProjectForm();


        await loadProjects();


    } catch (error) {

        console.error(
            "Project creation error:",
            error
        );


        showWorkspaceMessage(
            error.message ||
            "PROJECT COULD NOT BE CREATED.",
            "error"
        );


    } finally {

        if (submitButton) {

            submitButton.disabled =
                false;

            submitButton.textContent =
                "SAVE PROJECT";

        }

    }

}


/* =========================================================
   CHANGE PROJECT STATUS
   ========================================================= */

async function changeProjectStatus(
    projectId,
    status
) {

    if (!projectId) {

        return;

    }


    try {

        await apiRequest(
            `/projects/${encodeURIComponent(
                projectId
            )}/status`,
            {
                method: "PATCH",

                body: JSON.stringify({
                    status
                })

            }
        );


        showWorkspaceMessage(
            `PROJECT STATUS CHANGED TO ${status}.`,
            "success"
        );


        await loadProjects();


    } catch (error) {

        console.error(
            "Project status update error:",
            error
        );


        showWorkspaceMessage(
            error.message ||
            "PROJECT STATUS COULD NOT BE UPDATED.",
            "error"
        );

    }

}


/* =========================================================
   DELETE PROJECT
   ========================================================= */

async function deleteProject(
    projectId
) {

    if (!projectId) {

        return;

    }


    const confirmed =
        window.confirm(
            "DELETE THIS PROJECT?"
        );


    if (!confirmed) {

        return;

    }


    try {

        await apiRequest(
            `/projects/${encodeURIComponent(
                projectId
            )}`,
            {
                method: "DELETE"
            }
        );


        showWorkspaceMessage(
            "PROJECT DELETED SUCCESSFULLY.",
            "success"
        );


        await loadProjects();


    } catch (error) {

        console.error(
            "Project deletion error:",
            error
        );


        showWorkspaceMessage(
            error.message ||
            "PROJECT COULD NOT BE DELETED.",
            "error"
        );

    }

}


/* =========================================================
   RESET PROJECT FORM
   ========================================================= */

function resetProjectForm() {

    const form =
        getElement(
            "projectForm"
        );


    if (form) {

        form.reset();

    }


    const projectType =
        getElement(
            "projectType"
        );

    if (projectType) {

        projectType.value =
            "GENERAL";

    }


    const projectStatus =
        getElement(
            "projectStatus"
        );

    if (projectStatus) {

        projectStatus.value =
            "ACTIVE";

    }


    const projectVisibility =
        getElement(
            "projectVisibility"
        );

    if (projectVisibility) {

        projectVisibility.value =
            "PRIVATE";

    }


    const projectCurrency =
        getElement(
            "projectCurrency"
        );

    if (projectCurrency) {

        projectCurrency.value =
            "INR";

    }

}


/* =========================================================
   SHOW / HIDE PROJECT FORM
   ========================================================= */

function setupProjectForm() {

    const createButton =
        getElement(
            "createProjectButton"
        );


    const cancelButton =
        getElement(
            "cancelProjectButton"
        );


    const panel =
        getElement(
            "projectCreatePanel"
        );


    const form =
        getElement(
            "projectForm"
        );


    if (
        createButton &&
        panel
    ) {

        createButton.addEventListener(
            "click",
            () => {

                panel.classList.toggle(
                    "is-visible"
                );

                if (
                    panel.classList.contains(
                        "is-visible"
                    )
                ) {

                    panel.scrollIntoView({
                        behavior:
                            "smooth",
                        block:
                            "start"
                    });

                }

            }
        );

    }


    if (
        cancelButton &&
        panel
    ) {

        cancelButton.addEventListener(
            "click",
            () => {

                resetProjectForm();

                panel.classList.remove(
                    "is-visible"
                );

            }
        );

    }


    if (form) {

        form.addEventListener(
            "submit",
            createProject
        );

    }

}


/* =========================================================
   LOGOUT
   ========================================================= */

async function logout() {

    const token =
        getAuthToken();


    const sessionId =
        getSessionId();


    try {

        if (token) {

            await publicApiRequest(
                "/auth/logout",
                {
                    method: "POST",

                    body: JSON.stringify({

                        token,

                        session_id:
                            sessionId || null

                    })

                }
            );

        }

    } catch (error) {

        console.error(
            "Logout API error:",
            error
        );

    } finally {

        handleAuthenticationExpired();


        window.location.href =
            "/login.html";

    }

}


/* =========================================================
   SETUP LOGOUT BUTTON
   ========================================================= */

function setupLogoutButton() {

    const button =
        getElement(
            "logoutButton"
        );


    if (!button) {

        return;

    }


    button.addEventListener(
        "click",
        logout
    );

}


/* =========================================================
   LEGACY LOGIN BUTTON
   ========================================================= */

function setupLoginButton() {

    const button =
        getElement(
            "loginButton"
        );


    if (!button) {

        return;

    }


    if (
        isAuthenticated()
    ) {

        showAuthenticatedWorkspace();

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
   INITIALIZE AUTHENTICATED APPLICATION
   ========================================================= */

async function initializeAuthenticatedApplication() {

    const authenticated =
        await validateAuthentication();


    if (!authenticated) {

        return;

    }


    setupProjectForm();

    setupLogoutButton();

    await loadProjects();

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


    await initializeAuthenticatedApplication();

}


/* =========================================================
   START APPLICATION
   ========================================================= */

if (
    document.readyState ===
    "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        initializeApplication
    );

} else {

    initializeApplication();

}
