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


    /* Face movement direction */

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

function getNearestLocation() {

    let nearest =
        null;

    let nearestDistance =
        Infinity;


    for (
        const location
        of locations
    ) {

        const dx =
            player.position.x -
            location.position.x;

        const dz =
            player.position.z -
            location.position.z;


        const distance =
            Math.sqrt(
                dx * dx +
                dz * dz
            );


        if (
            distance <
            nearestDistance
        ) {

            nearest =
                location;

            nearestDistance =
                distance;
        }
    }


    return {
        location:
            nearest,

        distance:
            nearestDistance
    };
}


/* =========================================================
   INTERACTION
   ========================================================= */

function interact() {

    const result =
        getNearestLocation();


    if (
        !result.location ||
        result.distance > 18
    ) {
        return;
    }


    const data =
        result.location.userData;


    interactionTitle.textContent =
        data.name;


    interactionDescription.textContent =
        data.description;


    interactionPanel.classList.remove(
        "hidden"
    );
}


interactionClose.addEventListener(
    "click",
    () => {

        interactionPanel.classList.add(
            "hidden"
        );
    }
);


/* =========================================================
   HUD
   ========================================================= */

function updateStatus() {

    const result =
        getNearestLocation();


    if (
        result.location &&
        result.distance <= 18
    ) {

        runtimeStatus.textContent =
            `${result.location.userData.name} — PRESS E`;

        return;
    }


    runtimeStatus.textContent =
        "MUKTI MAHAL — EXPLORE";
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
    player.position
);


/* =========================================================
   GAME LOOP
   ========================================================= */

function animate() {

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
}


/* =========================================================
   START
   ========================================================= */

runtimeStatus.textContent =
    "MUKTI MAHAL — PLAYABLE WORLD";


animate();
