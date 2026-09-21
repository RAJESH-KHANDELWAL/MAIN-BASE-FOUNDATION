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
