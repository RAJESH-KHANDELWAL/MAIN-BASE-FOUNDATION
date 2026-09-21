import * as THREE from
    "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";

const canvas =
    document.getElementById("mahal-canvas");

const runtimeStatus =
    document.getElementById("runtime-status");

const interactionPanel =
    document.getElementById("interaction-panel");

const interactionTitle =
    document.getElementById("interaction-title");

const interactionDescription =
    document.getElementById("interaction-description");

const interactionClose =
    document.getElementById("interaction-close");

const mobileInteract =
    document.getElementById("mobile-interact");


/* =========================================================
   MUKTI MAHAL
   PLAYABLE DIGITAL WORLD
   ========================================================= */

const scene =
    new THREE.Scene();

scene.background =
    new THREE.Color(0x101010);

scene.fog =
    new THREE.Fog(
        0x101010,
        80,
        550
    );


/* =========================================================
   CAMERA
   ========================================================= */

const camera =
    new THREE.PerspectiveCamera(
        65,
        window.innerWidth /
            window.innerHeight,
        0.1,
        2000
    );


/* =========================================================
   RENDERER
   ========================================================= */

const renderer =
    new THREE.WebGLRenderer({
        canvas,
        antialias: true
    });

renderer.setPixelRatio(
    Math.min(
        window.devicePixelRatio || 1,
        2
    )
);

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);


/* =========================================================
   LIGHTING
   ========================================================= */

const ambientLight =
    new THREE.AmbientLight(
        0xffffff,
        1.7
    );

scene.add(
    ambientLight
);

const sunLight =
    new THREE.DirectionalLight(
        0xffffff,
        2.2
    );

sunLight.position.set(
    100,
    150,
    80
);

scene.add(
    sunLight
);


/* =========================================================
   WORLD ROOT
   ========================================================= */

const world =
    new THREE.Group();

scene.add(
    world
);


/* =========================================================
   GROUND
   ========================================================= */

const groundGeometry =
    new THREE.PlaneGeometry(
        1000,
        1000
    );

const groundMaterial =
    new THREE.MeshStandardMaterial({
        color: 0x303030,
        roughness: 1
    });

const ground =
    new THREE.Mesh(
        groundGeometry,
        groundMaterial
    );

ground.rotation.x =
    -Math.PI / 2;

ground.position.y =
    0;

world.add(
    ground
);


/* =========================================================
   GRID
   ========================================================= */

const grid =
    new THREE.GridHelper(
        1000,
        100,
        0x666666,
        0x333333
    );

grid.position.y =
    0.01;

world.add(
    grid
);


/* =========================================================
   LOCATIONS
   ========================================================= */

const locations = [];


function createBuilding({
    id,
    name,
    description,
    x,
    z,
    width,
    depth,
    height
}) {

    const geometry =
        new THREE.BoxGeometry(
            width,
            height,
            depth
        );

    const material =
        new THREE.MeshStandardMaterial({
            color: 0x555555,
            roughness: 0.8
        });

    const building =
        new THREE.Mesh(
            geometry,
            material
        );

    building.position.set(
        x,
        height / 2,
        z
    );

    building.userData = {
        id,
        name,
        description,
        interactive: true,
        width,
        depth
    };

    world.add(
        building
    );

    locations.push(
        building
    );

    return building;
}


/* =========================================================
   MUKTI MAHAL LOCATIONS
   ========================================================= */

createBuilding({
    id: "main-gate",
    name: "MUKTI MAHAL MAIN GATE",
    description:
        "The main entrance into the Mukti Mahal playable world.",
    x: 0,
    z: -90,
    width: 30,
    depth: 12,
    height: 10
});


createBuilding({
    id: "central-hall",
    name: "CENTRAL HALL",
    description:
        "The central gathering and activity area of Mukti Mahal.",
    x: 0,
    z: -35,
    width: 34,
    depth: 24,
    height: 12
});


createBuilding({
    id: "creator-studio",
    name: "CREATOR STUDIO",
    description:
        "Photography, video, design, music and digital creation space.",
    x: -55,
    z: 0,
    width: 25,
    depth: 20,
    height: 10
});


createBuilding({
    id: "cinema",
    name: "CINEMA",
    description:
        "The cinematic entertainment space of Mukti Mahal.",
    x: 55,
    z: 0,
    width: 25,
    depth: 20,
    height: 10
});


createBuilding({
    id: "gaming-area",
    name: "GAMING AREA",
    description:
        "An interactive entertainment area inside Mukti Mahal.",
    x: -55,
    z: 55,
    width: 25,
    depth: 20,
    height: 10
});


createBuilding({
    id: "music-room",
    name: "MUSIC ROOM",
    description:
        "Music and audio creation space.",
    x: 55,
    z: 55,
    width: 25,
    depth: 20,
    height: 10
});


/* =========================================================
   PLAYER
   ========================================================= */

const playerGeometry =
    new THREE.CapsuleGeometry(
        0.65,
        1.6,
        6,
        12
    );

const playerMaterial =
    new THREE.MeshStandardMaterial({
        color: 0xffffff,
        roughness: 0.6
    });

const player =
    new THREE.Mesh(
        playerGeometry,
        playerMaterial
    );

player.position.set(
    0,
    1.45,
    -115
);

world.add(
    player
);


const playerRadius =
    1.2;


/* =========================================================
   COLLISION
   ========================================================= */

function collidesWithBuilding(
    nextX,
    nextZ
) {

    for (
        const building
        of locations
    ) {

        const data =
            building.userData;

        const halfWidth =
            data.width / 2;

        const halfDepth =
            data.depth / 2;

        const minX =
            building.position.x -
            halfWidth -
            playerRadius;

        const maxX =
            building.position.x +
            halfWidth +
            playerRadius;

        const minZ =
            building.position.z -
            halfDepth -
            playerRadius;

        const maxZ =
            building.position.z +
            halfDepth +
            playerRadius;

        if (
            nextX >= minX &&
            nextX <= maxX &&
            nextZ >= minZ &&
            nextZ <= maxZ
        ) {
            return true;
        }
    }

    return false;
}


/* =========================================================
   INPUT
   ========================================================= */

const keys =
    new Set();


window.addEventListener(
    "keydown",
    event => {

        const key =
            event.key.toLowerCase();

        keys.add(
            key
        );

        if (
            key === "e"
        ) {
            interact();
        }
    }
);


window.addEventListener(
    "keyup",
    event => {

        keys.delete(
            event.key.toLowerCase()
        );
    }
);


/* =========================================================
   MOBILE CONTROLS
   ========================================================= */

document
    .querySelectorAll(
        "[data-key]"
    )
    .forEach(
        button => {

            const key =
                button.dataset.key;

            const start =
                event => {

                    event.preventDefault();

                    keys.add(
                        key
                    );
                };

            const stop =
                event => {

                    event.preventDefault();

                    keys.delete(
                        key
                    );
                };

            button.addEventListener(
                "pointerdown",
                start
            );

            button.addEventListener(
                "pointerup",
                stop
            );

            button.addEventListener(
                "pointercancel",
                stop
            );

            button.addEventListener(
                "pointerleave",
                stop
            );
        }
    );


mobileInteract.addEventListener(
    "click",
    () => {

        interact();
    }
);


/* =========================================================
   PLAYER MOVEMENT
   ========================================================= */

function updatePlayer() {

    let x =
        player.position.x;

    let z =
        player.position.z;

    let dx = 0;
    let dz = 0;


    if (
        keys.has("w") ||
        keys.has("arrowup")
    ) {
        dz -= 1;
    }


    if (
        keys.has("s") ||
        keys.has("arrowdown")
    ) {
        dz += 1;
    }


    if (
        keys.has("a") ||
        keys.has("arrowleft")
    ) {
        dx -= 1;
    }


    if (
        keys.has("d") ||
        keys.has("arrowright")
    ) {
        dx += 1;
    }


    if (
        dx === 0 &&
        dz === 0
    ) {
        return;
    }


    const length =
        Math.sqrt(
            dx * dx +
            dz * dz
        );


    dx /=
        length;

    dz /=
        length;


    let speed =
        0.22;


    if (
        keys.has("shift")
    ) {
        speed =
            0.42;
    }


    const nextX =
        x +
        dx *
        speed;


    const nextZ =
        z +
        dz *
        speed;


    if (
        !collidesWithBuilding(
            nextX,
            z
        )
    ) {

        x =
            nextX;
    }


    if (
        !collidesWithBuilding(
            x,
            nextZ
        )
    ) {

        z =
            nextZ;
    }


    player.position.x =
        x;

    player.position.z =
        z;


    if (
        dx !== 0 ||
        dz !== 0
    ) {

        player.rotation.y =
            Math.atan2(
                dx,
                dz
            );
    }
}


/* =========================================================
   CAMERA FOLLOW
   ========================================================= */

const cameraTarget =
    new THREE.Vector3();


const cameraDesired =
    new THREE.Vector3();


function updateCamera() {

    cameraTarget.set(
        player.position.x,
        player.position.y + 1.5,
        player.position.z
    );


    cameraDesired.set(
        player.position.x,
        player.position.y + 9,
        player.position.z + 14
    );


    camera.position.lerp(
        cameraDesired,
        0.08
    );


    camera.lookAt(
        cameraTarget
    );
}
/* =========================================================
   NEAREST LOCATION
   ========================================================= */

let nearestLocation = null;


function findNearestLocation() {

    let nearest =
        null;

    let nearestDistance =
        Infinity;


    for (
        const location
        of locations
    ) {

        const distance =
            player.position.distanceTo(
                location.position
            );


        if (
            distance <
            nearestDistance
        ) {

            nearestDistance =
                distance;

            nearest =
                location;
        }
    }


    nearestLocation =
        nearest;


    return nearest;
}


/* =========================================================
   INTERACTION
   ========================================================= */

function interact() {

    const location =
        findNearestLocation();


    if (!location) {
        return;
    }


    const distance =
        player.position.distanceTo(
            location.position
        );


    if (
        distance >
        35
    ) {

        runtimeStatus.textContent =
            "Move closer to a location to interact.";

        return;
    }


    interactionTitle.textContent =
        location.userData.name;


    interactionDescription.textContent =
        location.userData.description;


    interactionPanel.classList.add(
        "active"
    );


    runtimeStatus.textContent =
        `INTERACTING — ${location.userData.name}`;
}


/* =========================================================
   CLOSE INTERACTION
   ========================================================= */

interactionClose.addEventListener(
    "click",
    () => {

        interactionPanel.classList.remove(
            "active"
        );

        runtimeStatus.textContent =
            cinematicMode
                ? "MUKTI MAHAL — CINEMATIC MOVIE MODE"
                : "MUKTI MAHAL — GAME MODE";
    }
);


/* =========================================================
   STATUS / LOCATION HUD
   ========================================================= */

function updateStatus() {

    const location =
        findNearestLocation();


    if (!location) {
        return;
    }


    const distance =
        player.position.distanceTo(
            location.position
        );


    if (
        distance <= 35
    ) {

        runtimeStatus.textContent =
            `${location.userData.name} — PRESS E TO ENTER`;
    }
    else {

        runtimeStatus.textContent =
            "MUKTI MAHAL — GAME MODE";
    }
}


/* =========================================================
   RESIZE
   ========================================================= */

window.addEventListener(
    "resize",
    () => {

        camera.aspect =
            window.innerWidth /
            window.innerHeight;


        camera.updateProjectionMatrix();


        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );


        renderer.setPixelRatio(
            Math.min(
                window.devicePixelRatio || 1,
                2
            )
        );
    }
);


/* =========================================================
   INITIAL CAMERA
   ========================================================= */

camera.position.set(
    0,
    9,
    -101
);


camera.lookAt(
    0,
    3,
    -90
);


/* =========================================================
   MUKTI MAHAL CINEMATIC MODE
   GAME + MOVIE CAMERA
   ========================================================= */

let cinematicMode =
    false;

let cinematicIndex =
    0;

let cinematicElapsed =
    0;


const cinematicShots = [

    {
        position:
            new THREE.Vector3(
                0,
                16,
                -150
            ),

        target:
            new THREE.Vector3(
                0,
                7,
                -70
            ),

        duration:
            7
    },


    {
        position:
            new THREE.Vector3(
                58,
                13,
                -82
            ),

        target:
            new THREE.Vector3(
                0,
                10,
                -35
            ),

        duration:
            7
    },


    {
        position:
            new THREE.Vector3(
                105,
                20,
                28
            ),

        target:
            new THREE.Vector3(
                0,
                10,
                0
            ),

        duration:
            8
    },


    {
        position:
            new THREE.Vector3(
                -105,
                20,
                70
            ),

        target:
            new THREE.Vector3(
                0,
                9,
                35
            ),

        duration:
            8
    },


    {
        position:
            new THREE.Vector3(
                0,
                24,
                145
            ),

        target:
            new THREE.Vector3(
                0,
                8,
                35
            ),

        duration:
            8
    }

];


function setCinematicMode(
    enabled
) {

    cinematicMode =
        enabled;


    cinematicIndex =
        0;


    cinematicElapsed =
        0;


    if (
        cinematicMode
    ) {

        keys.clear();


        runtimeStatus.textContent =
            "MUKTI MAHAL — CINEMATIC MOVIE MODE";

    }
    else {

        runtimeStatus.textContent =
            "MUKTI MAHAL — GAME MODE";


        updateCamera();
    }
}


/* =========================================================
   CINEMATIC CAMERA UPDATE
   ========================================================= */

function updateCinematic(
    delta
) {

    if (
        !cinematicMode
    ) {
        return;
    }


    const shot =
        cinematicShots[
            cinematicIndex
        ];


    cinematicElapsed +=
        delta;


    const progress =
        Math.min(
            cinematicElapsed /
                shot.duration,
            1
        );


    const eased =
        progress *
        progress *
        (3 - 2 * progress);


    camera.position.lerp(
        shot.position,
        0.018 +
        eased *
        0.012
    );


    camera.lookAt(
        shot.target
    );


    if (
        cinematicElapsed >=
        shot.duration
    ) {

        cinematicIndex =
            (
                cinematicIndex +
                1
            ) %
            cinematicShots.length;


        cinematicElapsed =
            0;
    }
}


/* =========================================================
   CINEMATIC KEY CONTROLS
   C = CINEMATIC MODE
   ESC = GAME MODE
   ========================================================= */

window.addEventListener(
    "keydown",
    event => {

        const key =
            event.key.toLowerCase();


        if (
            key === "c"
        ) {

            setCinematicMode(
                !cinematicMode
            );
        }


        if (
            key === "escape" &&
            cinematicMode
        ) {

            setCinematicMode(
                false
            );
        }
    }
);


/* =========================================================
   GAME LOOP
   ========================================================= */

let previousFrameTime =
    performance.now();


function animate() {

    requestAnimationFrame(
        animate
    );


    const now =
        performance.now();


    const delta =
        Math.min(
            (
                now -
                previousFrameTime
            ) / 1000,
            0.05
        );


    previousFrameTime =
        now;


    if (
        !cinematicMode
    ) {

        updatePlayer();

        updateCamera();

        updateStatus();
    }


    updateCinematic(
        delta
    );


    renderer.render(
        scene,
        camera
    );
}


/* =========================================================
   START MUKTI MAHAL
   ========================================================= */

animate();






cd /workspaces/MAIN-BASE-FOUNDATION

python3 - <<'PY'
from pathlib import Path

p = Path("frontend/mukti-mahal.js")

if not p.exists():
    raise SystemExit("ERROR: frontend/mukti-mahal.js NOT FOUND")

s = p.read_text(encoding="utf-8")

if "MUKTI_MAHAL_CINEMATIC_ENGINE_V1" in s:
    raise SystemExit("ALREADY PATCHED: MUKTI_MAHAL_CINEMATIC_ENGINE_V1")

anchor = "/* =========================================================\n   GAME LOOP\n   ========================================================= */"

if anchor not in s:
    raise SystemExit("ERROR: GAME LOOP anchor NOT FOUND")

block = r'''
/* =========================================================
   MUKTI_MAHAL_CINEMATIC_ENGINE_V1
   GAME + MOVIE + CINEMATIC WORLD
   ========================================================= */

renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;

scene.background = new THREE.Color(0x080b12);

scene.fog = new THREE.FogExp2(
    0x101722,
    0.00125
);


/* =========================================================
   REALISTIC WORLD LIGHTING
   ========================================================= */

const moonLight =
    new THREE.HemisphereLight(
        0x9bbcff,
        0x24180e,
        1.15
    );

scene.add(moonLight);


const warmSun =
    new THREE.DirectionalLight(
        0xffe2b8,
        2.8
    );

warmSun.position.set(
    -180,
    240,
    -120
);

warmSun.castShadow = true;

scene.add(warmSun);


/* =========================================================
   REMOVE DEBUG GRID
   ========================================================= */

grid.visible = false;


/* =========================================================
   PREMIUM GROUND
   ========================================================= */

ground.material =
    new THREE.MeshStandardMaterial({
        color: 0x5b5046,
        roughness: 0.72,
        metalness: 0.05
    });


/* =========================================================
   MATERIALS
   ========================================================= */

const palaceStone =
    new THREE.MeshStandardMaterial({
        color: 0xc8a878,
        roughness: 0.58,
        metalness: 0.02
    });

const palaceDark =
    new THREE.MeshStandardMaterial({
        color: 0x4b3325,
        roughness: 0.65
    });

const goldMaterial =
    new THREE.MeshStandardMaterial({
        color: 0xc89438,
        roughness: 0.28,
        metalness: 0.7
    });

const waterMaterial =
    new THREE.MeshPhysicalMaterial({
        color: 0x173d52,
        roughness: 0.12,
        metalness: 0.15,
        transmission: 0.15,
        transparent: true,
        opacity: 0.88
    });

const glassMaterial =
    new THREE.MeshPhysicalMaterial({
        color: 0x9cc7d9,
        roughness: 0.12,
        metalness: 0.1,
        transmission: 0.45,
        transparent: true,
        opacity: 0.58
    });


/* =========================================================
   DECORATIVE BUILDING FACADE
   ========================================================= */

function addFacade(building) {

    const data = building.userData;

    building.material = palaceStone;

    const facade =
        new THREE.Group();

    facade.position.copy(
        building.position
    );

    const width =
        data.width;

    const depth =
        data.depth;

    const height =
        data.height;


    /* Main entrance */

    const entrance =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                Math.min(width * 0.32, 10),
                height * 0.78,
                1.2
            ),
            palaceDark
        );

    entrance.position.set(
        0,
        -height * 0.05,
        depth / 2 + 0.7
    );

    facade.add(entrance);


    /* Columns */

    const columnGeometry =
        new THREE.CylinderGeometry(
            0.55,
            0.7,
            height * 0.9,
            16
        );

    const columnPositions = [
        -width * 0.38,
        -width * 0.19,
        width * 0.19,
        width * 0.38
    ];

    for (
        const x of columnPositions
    ) {

        const column =
            new THREE.Mesh(
                columnGeometry,
                palaceStone
            );

        column.position.set(
            x,
            0,
            depth / 2 + 1.1
        );

        facade.add(column);
    }


    /* Upper cornice */

    const cornice =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                width * 0.92,
                1.1,
                2.0
            ),
            goldMaterial
        );

    cornice.position.set(
        0,
        height * 0.44,
        depth / 2 + 1.0
    );

    facade.add(cornice);


    /* Dome */

    const dome =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                Math.min(width, depth) * 0.18,
                32,
                18,
                0,
                Math.PI * 2,
                0,
                Math.PI / 2
            ),
            palaceStone
        );

    dome.position.set(
        0,
        height + Math.min(width, depth) * 0.12,
        0
    );

    facade.add(dome);


    /* Dome finial */

    const finial =
        new THREE.Mesh(
            new THREE.ConeGeometry(
                0.65,
                2.2,
                16
            ),
            goldMaterial
        );

    finial.position.set(
        0,
        height + Math.min(width, depth) * 0.28,
        0
    );

    facade.add(finial);


    /* Side domes */

    for (
        const x of [
            -width * 0.38,
            width * 0.38
        ]
    ) {

        const sideDome =
            new THREE.Mesh(
                new THREE.SphereGeometry(
                    2.6,
                    24,
                    16,
                    0,
                    Math.PI * 2,
                    0,
                    Math.PI / 2
                ),
                palaceStone
            );

        sideDome.position.set(
            x,
            height + 1.0,
            0
        );

        facade.add(sideDome);
    }


    world.add(facade);

    return facade;
}


for (
    const building
    of locations
) {
    addFacade(building);
}


/* =========================================================
   WATER POOLS
   ========================================================= */

function createPool(
    x,
    z,
    width,
    depth
) {

    const pool =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                width,
                0.45,
                depth
            ),
            waterMaterial
        );

    pool.position.set(
        x,
        0.28,
        z
    );

    world.add(pool);


    const border =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                width + 2,
                0.55,
                depth + 2
            ),
            palaceStone
        );

    border.position.set(
        x,
        0.18,
        z
    );

    world.add(border);

    return pool;
}


createPool(
    0,
    -72,
    42,
    10
);

createPool(
    -32,
    -10,
    18,
    8
);

createPool(
    32,
    -10,
    18,
    8
);


/* =========================================================
   FOUNTAINS
   ========================================================= */

function createFountain(
    x,
    z
) {

    const base =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                4,
                4.6,
                0.8,
                32
            ),
            palaceStone
        );

    base.position.set(
        x,
        0.45,
        z
    );

    world.add(base);


    const water =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                3.2,
                3.2,
                0.18,
                32
            ),
            waterMaterial
        );

    water.position.set(
        x,
        0.9,
        z
    );

    world.add(water);


    const pillar =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                0.5,
                0.75,
                4,
                20
            ),
            palaceStone
        );

    pillar.position.set(
        x,
        2.5,
        z
    );

    world.add(pillar);


    const glow =
        new THREE.PointLight(
            0xffc66d,
            4,
            25
        );

    glow.position.set(
        x,
        4.5,
        z
    );

    world.add(glow);
}


createFountain(
    0,
    -58
);

createFountain(
    -28,
    -62
);

createFountain(
    28,
    -62
);


/* =========================================================
   LANTERNS
   ========================================================= */

function createLantern(
    x,
    z
) {

    const pole =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                0.08,
                0.12,
                3.2,
                12
            ),
            goldMaterial
        );

    pole.position.set(
        x,
        1.6,
        z
    );

    world.add(pole);


    const light =
        new THREE.PointLight(
            0xffb45c,
            2.2,
            16
        );

    light.position.set(
        x,
        3.1,
        z
    );

    world.add(light);


    const bulb =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                0.25,
                16,
                16
            ),
            new THREE.MeshBasicMaterial({
                color: 0xffd27a
            })
        );

    bulb.position.copy(
        light.position
    );

    world.add(bulb);
}


for (
    let z = -105;
    z <= 80;
    z += 18
) {

    createLantern(-16, z);
    createLantern(16, z);
}


/* =========================================================
   TREES / GREENERY
   ========================================================= */

function createTree(
    x,
    z,
    scale = 1
) {

    const trunk =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                0.45 * scale,
                0.7 * scale,
                5 * scale,
                10
            ),
            palaceDark
        );

    trunk.position.set(
        x,
        2.5 * scale,
        z
    );

    world.add(trunk);


    const crown =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                2.8 * scale,
                20,
                16
            ),
            new THREE.MeshStandardMaterial({
                color: 0x214d2e,
                roughness: 0.95
            })
        );

    crown.position.set(
        x,
        6 * scale,
        z
    );

    world.add(crown);
}


const treePositions = [
    [-28, -92],
    [28, -92],
    [-38, -72],
    [38, -72],
    [-42, -42],
    [42, -42],
    [-75, -20],
    [75, -20],
    [-78, 35],
    [78, 35],
    [-30, 82],
    [30, 82]
];


for (
    const [x, z]
    of treePositions
) {
    createTree(
        x,
        z,
        1
    );
}


/* =========================================================
   ATMOSPHERIC STARS
   ========================================================= */

const starCount = 1800;

const starPositions =
    new Float32Array(
        starCount * 3
    );

for (
    let i = 0;
    i < starCount;
    i++
) {

    const i3 =
        i * 3;

    starPositions[i3] =
        (Math.random() - 0.5) * 1400;

    starPositions[i3 + 1] =
        120 +
        Math.random() * 400;

    starPositions[i3 + 2] =
        (Math.random() - 0.5) * 1400;
}


const starGeometry =
    new THREE.BufferGeometry();

starGeometry.setAttribute(
    "position",
    new THREE.BufferAttribute(
        starPositions,
        3
    )
);


const starMaterial =
    new THREE.PointsMaterial({
        color: 0xffffff,
        size: 1.2,
        transparent: true,
        opacity: 0.7,
        sizeAttenuation: true
    });


const stars =
    new THREE.Points(
        starGeometry,
        starMaterial
    );

scene.add(stars);


/* =========================================================
   CINEMATIC CAMERA SYSTEM
   ========================================================= */

let cinematicMode = false;

let cinematicTime = 0;

let cinematicIndex = 0;

const cinematicPoints = [

    {
        position:
            new THREE.Vector3(
                0,
                18,
                -145
            ),

        target:
            new THREE.Vector3(
                0,
                10,
                -70
            ),

        duration: 7
    },

    {
        position:
            new THREE.Vector3(
                55,
                12,
                -80
            ),

        target:
            new THREE.Vector3(
                0,
                12,
                -35
            ),

        duration: 7
    },

    {
        position:
            new THREE.Vector3(
                100,
                18,
                30
            ),

        target:
            new THREE.Vector3(
                0,
                12,
                0
            ),

        duration: 8
    },

    {
        position:
            new THREE.Vector3(
                -100,
                20,
                70
            ),

        target:
            new THREE.Vector3(
                0,
                10,
                35
            ),

        duration: 8
    },

    {
        position:
            new THREE.Vector3(
                0,
                24,
                150
            ),

        target:
            new THREE.Vector3(
                0,
                8,
                35
            ),

        duration: 8
    }
];


function setCinematicMode(
    enabled
) {

    cinematicMode =
        enabled;

    cinematicTime =
        0;

    cinematicIndex =
        0;

    if (
        cinematicMode
    ) {

        runtimeStatus.textContent =
            "MUKTI MAHAL — CINEMATIC MOVIE MODE";

        keys.clear();

        camera.position.copy(
            cinematicPoints[0].position
        );

        camera.lookAt(
            cinematicPoints[0].target
        );

    } else {

        runtimeStatus.textContent =
            "MUKTI MAHAL — GAME MODE";
    }
}


function updateCinematic(
    delta
) {

    if (
        !cinematicMode
    ) {
        return;
    }


    const point =
        cinematicPoints[
            cinematicIndex
        ];

    cinematicTime +=
        delta;


    const progress =
        Math.min(
            cinematicTime /
            point.duration,
            1
        );


    const eased =
        progress *
        progress *
        (3 - 2 * progress);


    camera.position.lerpVectors(
        camera.position,
        point.position,
        0.025 + eased * 0.015
    );


    camera.lookAt(
        point.target
    );


    if (
        cinematicTime >=
        point.duration
    ) {

        cinematicIndex =
            (
                cinematicIndex + 1
            ) %
            cinematicPoints.length;

        cinematicTime =
            0;
    }
}


/* =========================================================
   CINEMATIC / GAME CONTROLS
   ========================================================= */

window.addEventListener(
    "keydown",
    event => {

        const key =
            event.key.toLowerCase();

        if (
            key === "c"
        ) {

            setCinematicMode(
                !cinematicMode
            );
        }

        if (
            key === "escape" &&
            cinematicMode
        ) {

            setCinematicMode(
                false
            );
        }
    }
);


/* =========================================================
   CAMERA QUALITY
   ========================================================= */

camera.fov = 68;

camera.updateProjectionMatrix();


/* =========================================================
   FRAME TIMING
   ========================================================= */

let previousTime =
    performance.now();

function cinematicDelta() {

    const now =
        performance.now();

    const delta =
        Math.min(
            (now - previousTime) /
            1000,
            0.05
        );

    previousTime =
        now;

    return delta;
}

'''

s = s.replace(
    anchor,
    block + "\n\n" + anchor
)

# Replace the existing animate function with a delta-aware version.
old = '''function animate() {

    requestAnimationFrame(
        animate
    );


    updatePlayer();

    updateCamera();

    updateStatus();


    renderer.render(
        scene,
        camera
    );
}'''

new = '''function animate() {

    requestAnimationFrame(
        animate
    );

    const delta =
        cinematicDelta();

    if (!cinematicMode) {
        updatePlayer();
        updateCamera();
        updateStatus();
    }

    updateCinematic(delta);

    renderer.render(
        scene,
        camera
    );
}'''

if old not in s:
    raise SystemExit("ERROR: existing animate() block NOT FOUND")

s = s.replace(old, new)

p.write_text(s, encoding="utf-8")

print("SUCCESS: frontend/mukti-mahal.js upgraded")
print("MODE: GAME + CINEMATIC MOVIE")
print("KEY: C = CINEMATIC MODE")
print("KEY: ESC = GAME MODE")
PY

node --check frontend/mukti-mahal.js
git diff --stat -- frontend/mukti-mahal.js
