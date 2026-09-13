const INFRASTRUCTURE_CONTROL_PLANE_API =
    "https://rajeshkhandelwalofficial.onrender.com";


const infrastructureControlPlaneStatus =
    document.getElementById(
        "infrastructure-control-plane-status"
    );


const infrastructureControlPlaneData =
    document.getElementById(
        "infrastructure-control-plane-data"
    );


const infrastructureControlPlaneUpdated =
    document.getElementById(
        "infrastructure-control-plane-updated"
    );


function setInfrastructureControlPlaneStatus(
    text
) {
    if (infrastructureControlPlaneStatus) {
        infrastructureControlPlaneStatus.textContent = text;
    }
}


function setInfrastructureCount(
    id,
    value
) {
    const element =
        document.getElementById(id);

    if (element) {
        element.textContent =
            value ?? 0;
    }
}


async function fetchInfrastructure(
    endpoint
) {
    const url =
        `${INFRASTRUCTURE_CONTROL_PLANE_API}${endpoint}`;

    try {
        const response =
            await fetch(
                url,
                {
                    method: "GET",
                    headers: {
                        "Accept": "application/json"
                    },
                    cache: "no-store"
                }
            );

        const contentType =
            response.headers.get(
                "content-type"
            ) || "";

        const responseText =
            await response.text();

        if (!response.ok) {
            throw new Error(
                `${response.status} ${response.statusText}: ${responseText}`
            );
        }

        if (
            !contentType.includes(
                "application/json"
            )
        ) {
            throw new Error(
                `Expected JSON but received ${contentType || "unknown content type"}`
            );
        }

        return JSON.parse(
            responseText
        );

    } catch (error) {

        console.error(
            "Infrastructure API request failed:",
            endpoint,
            error
        );

        throw error;
    }
}


function renderInfrastructureTable(
    title,
    records
) {
    if (
        !records ||
        !Array.isArray(records) ||
        records.length === 0
    ) {
        return `
            <div class="infrastructure-control-plane-empty">
                <strong>${title}</strong>
                <p>No records available yet.</p>
            </div>
        `;
    }


    const columns =
        Object.keys(records[0]);


    const header =
        columns
            .map(
                column =>
                    `<th>${column
                        .replaceAll("_", " ")
                        .toUpperCase()}</th>`
            )
            .join("");


    const rows =
        records
            .map(
                record => {

                    const cells =
                        columns
                            .map(
                                column => {

                                    let value =
                                        record[column];


                                    if (
                                        typeof value ===
                                            "object" &&
                                        value !== null
                                    ) {
                                        value =
                                            JSON.stringify(
                                                value
                                            );
                                    }


                                    return `
                                        <td>
                                            ${value ?? "—"}
                                        </td>
                                    `;
                                }
                            )
                            .join("");


                    return `
                        <tr>
                            ${cells}
                        </tr>
                    `;
                }
            )
            .join("");


    return `
        <h3>${title}</h3>

        <table class="infrastructure-control-plane-table">

            <thead>
                <tr>
                    ${header}
                </tr>
            </thead>

            <tbody>
                ${rows}
            </tbody>

        </table>
    `;
}


function renderInfrastructureError(
    title,
    error
) {
    const message =
        error instanceof Error
            ? error.message
            : String(error);


    return `
        <div class="infrastructure-control-plane-empty">

            <strong>
                ${title}
            </strong>

            <p>
                API ERROR:
                ${message}
            </p>

        </div>
    `;
}


async function loadInfrastructureControlPlane() {

    setInfrastructureControlPlaneStatus(
        "LOADING..."
    );


    if (infrastructureControlPlaneData) {
        infrastructureControlPlaneData.innerHTML =
            `
                <div class="infrastructure-control-plane-empty">
                    <strong>
                        Loading live infrastructure data...
                    </strong>
                </div>
            `;
    }


    /*
     * ------------------------------------------------------------
     * SUMMARY
     * ------------------------------------------------------------
     */

    let summary = null;


    try {

        summary =
            await fetchInfrastructure(
                "/infrastructure/summary"
            );

    } catch (error) {

        console.error(
            "Infrastructure Summary Error:",
            error
        );

        setInfrastructureControlPlaneStatus(
            "API ERROR"
        );


        if (
            infrastructureControlPlaneData
        ) {

            infrastructureControlPlaneData.innerHTML =
                renderInfrastructureError(
                    "INFRASTRUCTURE SUMMARY",
                    error
                );

        }

        if (
            infrastructureControlPlaneUpdated
        ) {
            infrastructureControlPlaneUpdated.textContent =
                `ERROR ${new Date().toLocaleString()}`;
        }

        return;
    }


    const counts =
        summary &&
        summary.counts
            ? summary.counts
            : {};


    setInfrastructureCount(
        "infrastructure-domains-count",
        counts.domains
    );


    setInfrastructureCount(
        "infrastructure-hosting-count",
        counts.hosting
    );


    setInfrastructureCount(
        "infrastructure-servers-count",
        counts.servers
    );


    setInfrastructureCount(
        "infrastructure-ipam-count",
        counts.ip_addresses
    );


    setInfrastructureCount(
        "infrastructure-network-count",
        counts.networks
    );


    setInfrastructureCount(
        "infrastructure-dns-zones-count",
        counts.dns_zones
    );


    setInfrastructureCount(
        "infrastructure-dns-records-count",
        counts.dns_records
    );


    /*
     * ------------------------------------------------------------
     * INFRASTRUCTURE MODULES
     * ------------------------------------------------------------
     */

    const infrastructureRequests = {

        "DOMAINS":
            "/infrastructure/domains",

        "HOSTING":
            "/infrastructure/hosting",

        "SERVERS":
            "/infrastructure/servers",

        "IPAM":
            "/infrastructure/ipam",

        "NETWORK":
            "/infrastructure/network",

        "DNS ZONES":
            "/infrastructure/dns/zones",

        "DNS RECORDS":
            "/infrastructure/dns/records"

    };


    const infrastructureResults = {};


    for (
        const [
            title,
            endpoint
        ]
        of Object.entries(
            infrastructureRequests
        )
    ) {

        try {

            infrastructureResults[title] =
                {
                    success: true,
                    data:
                        await fetchInfrastructure(
                            endpoint
                        )
                };

        } catch (error) {

            infrastructureResults[title] =
                {
                    success: false,
                    error: error
                };

        }

    }


    /*
     * ------------------------------------------------------------
     * RENDER ALL MODULES
     * ------------------------------------------------------------
     */

    let html = "";


    for (
        const [
            title
        ]
        of Object.keys(
            infrastructureRequests
        )
    ) {

        const result =
            infrastructureResults[
                title
            ];


        if (
            result &&
            result.success
        ) {

            html +=
                renderInfrastructureTable(
                    title,
                    result.data
                );

        } else {

            html +=
                renderInfrastructureError(
                    title,
                    result.error
                );

        }

    }


    if (
        infrastructureControlPlaneData
    ) {

        infrastructureControlPlaneData.innerHTML =
            html;

    }


    /*
     * ------------------------------------------------------------
     * FINAL STATUS
     * ------------------------------------------------------------
     */

    const failedModules =
        Object.entries(
            infrastructureResults
        )
        .filter(
            (
                [
                    ,
                    result
                ]
            ) =>
                !result.success
        )
        .map(
            (
                [
                    title
                ]
            ) =>
                title
        );


    if (
        failedModules.length === 0
    ) {

        setInfrastructureControlPlaneStatus(
            "LIVE"
        );

    } else {

        setInfrastructureControlPlaneStatus(
            `PARTIAL ERROR — ${failedModules.join(", ")}`
        );

    }


    if (
        infrastructureControlPlaneUpdated
    ) {

        infrastructureControlPlaneUpdated.textContent =
            `UPDATED ${new Date().toLocaleString()}`;

    }
}


/*
 * ------------------------------------------------------------
 * REFRESH BUTTON
 * ------------------------------------------------------------
 */

const infrastructureControlPlaneRefresh =
    document.getElementById(
        "infrastructure-control-plane-refresh"
    );


if (
    infrastructureControlPlaneRefresh
) {

    infrastructureControlPlaneRefresh.addEventListener(
        "click",
        loadInfrastructureControlPlane
    );

}


/*
 * ------------------------------------------------------------
 * INITIAL LOAD
 * ------------------------------------------------------------
 */

loadInfrastructureControlPlane();
