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
    infrastructureControlPlaneStatus.textContent = text;
}


function setInfrastructureCount(
    id,
    value
) {
    const element = document.getElementById(id);

    if (element) {
        element.textContent = value ?? 0;
    }
}


async function fetchInfrastructure(
    endpoint
) {
    const response = await fetch(
        `${INFRASTRUCTURE_CONTROL_PLANE_API}${endpoint}`,
        {
            method: "GET",
            headers: {
                "Accept": "application/json"
            },
            cache: "no-store"
        }
    );

    if (!response.ok) {
        throw new Error(
            `Infrastructure API error: ${response.status}`
        );
    }

    return response.json();
}


function renderInfrastructureTable(
    title,
    records
) {
    if (!records || records.length === 0) {
        return `
            <div class="infrastructure-control-plane-empty">
                <strong>${title}</strong>
                <p>No records available yet.</p>
            </div>
        `;
    }

    const columns = Object.keys(records[0]);

    const header = columns
        .map(
            column =>
                `<th>${column.replaceAll("_", " ").toUpperCase()}</th>`
        )
        .join("");

    const rows = records
        .map(record => {
            const cells = columns
                .map(column => {
                    let value = record[column];

                    if (
                        typeof value === "object" &&
                        value !== null
                    ) {
                        value = JSON.stringify(value);
                    }

                    return `<td>${value ?? "—"}</td>`;
                })
                .join("");

            return `<tr>${cells}</tr>`;
        })
        .join("");

    return `
        <h3>${title}</h3>

        <table class="infrastructure-control-plane-table">
            <thead>
                <tr>${header}</tr>
            </thead>

            <tbody>
                ${rows}
            </tbody>
        </table>
    `;
}


async function loadInfrastructureControlPlane() {
    try {
        setInfrastructureControlPlaneStatus(
            "LOADING..."
        );

        infrastructureControlPlaneData.textContent =
            "Loading live infrastructure data...";

        const summary =
            await fetchInfrastructure(
                "/infrastructure/summary"
            );

        const counts = summary.counts || {};

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


        const [
            domains,
            hosting,
            servers,
            ipam,
            network,
            dnsZones,
            dnsRecords
        ] = await Promise.all([
            fetchInfrastructure(
                "/infrastructure/domains"
            ),

            fetchInfrastructure(
                "/infrastructure/hosting"
            ),

            fetchInfrastructure(
                "/infrastructure/servers"
            ),

            fetchInfrastructure(
                "/infrastructure/ipam"
            ),

            fetchInfrastructure(
                "/infrastructure/network"
            ),

            fetchInfrastructure(
                "/infrastructure/dns/zones"
            ),

            fetchInfrastructure(
                "/infrastructure/dns/records"
            )
        ]);


        infrastructureControlPlaneData.innerHTML = `
            ${renderInfrastructureTable(
                "DOMAINS",
                domains
            )}

            ${renderInfrastructureTable(
                "HOSTING",
                hosting
            )}

            ${renderInfrastructureTable(
                "SERVERS",
                servers
            )}

            ${renderInfrastructureTable(
                "IPAM",
                ipam
            )}

            ${renderInfrastructureTable(
                "NETWORK",
                network
            )}

            ${renderInfrastructureTable(
                "DNS ZONES",
                dnsZones
            )}

            ${renderInfrastructureTable(
                "DNS RECORDS",
                dnsRecords
            )}
        `;


        setInfrastructureControlPlaneStatus(
            "LIVE"
        );

        infrastructureControlPlaneUpdated.textContent =
            `UPDATED ${new Date().toLocaleString()}`;

    } catch (error) {

        console.error(
            "Infrastructure Control Plane:",
            error
        );

        setInfrastructureControlPlaneStatus(
            "ERROR"
        );

        infrastructureControlPlaneData.innerHTML = `
            <div class="infrastructure-control-plane-empty">
                <strong>
                    Infrastructure API unavailable
                </strong>

                <p>
                    The control plane could not load live data.
                </p>
            </div>
        `;
    }
}


document
    .getElementById(
        "infrastructure-control-plane-refresh"
    )
    .addEventListener(
        "click",
        loadInfrastructureControlPlane
    );


loadInfrastructureControlPlane();
