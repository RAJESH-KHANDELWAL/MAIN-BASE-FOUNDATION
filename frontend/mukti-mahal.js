(() => {
    "use strict";

    const canvas = document.getElementById("mahal-canvas");
    const ctx = canvas.getContext("2d");

    const status = document.getElementById("runtime-status");
    const panel = document.getElementById("interaction-panel");
    const interactionTitle = document.getElementById("interaction-title");
    const interactionDescription =
        document.getElementById("interaction-description");
    const closeInteraction =
        document.getElementById("close-interaction");

    const keys = new Set();

    const player = {
        x: 0,
        y: 0,
        speed: 3.5,
        size: 18
    };

    const places = [
        {
            id: "main-gate",
            x: 0,
            y: -260,
            width: 180,
            height: 70,
            title: "Mukti Mahal Main Gate",
            description:
                "The main entrance of Mukti Mahal."
        },
        {
            id: "central-hall",
            x: 0,
            y: -80,
            width: 240,
            height: 120,
            title: "Central Hall",
            description:
                "The central space of the Mukti Mahal world."
        },
        {
            id: "creator-studio",
            x: -300,
            y: 80,
            width: 170,
            height: 100,
            title: "Creator Studio",
            description:
                "A creation space for photography, video, music and digital media."
        },
        {
            id: "cinema",
            x: 300,
            y: 80,
            width: 170,
            height: 100,
            title: "Cinema",
            description:
                "The cinematic creation and viewing area of Mukti Mahal."
        },
        {
            id: "gaming-area",
            x: -300,
            y: 280,
            width: 170,
            height: 100,
            title: "Gaming Area",
            description:
                "An interactive area inside the Mukti Mahal world."
        },
        {
            id: "music-room",
            x: 300,
            y: 280,
            width: 170,
            height: 100,
            title: "Music Room",
            description:
                "A space for music and audio creation."
        }
    ];

    function resize() {
        const ratio = window.devicePixelRatio || 1;

        canvas.width = window.innerWidth * ratio;
        canvas.height = window.innerHeight * ratio;

        canvas.style.width = `${window.innerWidth}px`;
        canvas.style.height = `${window.innerHeight}px`;

        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function isPressed(...names) {
        return names.some(name => keys.has(name));
    }

    function update() {
        let dx = 0;
        let dy = 0;

        if (isPressed("w", "W", "ArrowUp")) {
            dy -= 1;
        }

        if (isPressed("s", "S", "ArrowDown")) {
            dy += 1;
        }

        if (isPressed("a", "A", "ArrowLeft")) {
            dx -= 1;
        }

        if (isPressed("d", "D", "ArrowRight")) {
            dx += 1;
        }

        if (dx !== 0 || dy !== 0) {
            const length = Math.sqrt(dx * dx + dy * dy);

            player.x += (dx / length) * player.speed;
            player.y += (dy / length) * player.speed;
        }
    }

    function worldToScreen(x, y) {
        return {
            x: window.innerWidth / 2 + x - player.x,
            y: window.innerHeight / 2 + y - player.y
        };
    }

    function drawBackground() {
        ctx.fillStyle = "#101010";
        ctx.fillRect(
            0,
            0,
            window.innerWidth,
            window.innerHeight
        );

        ctx.strokeStyle = "rgba(255,255,255,0.05)";
        ctx.lineWidth = 1;

        const grid = 50;

        for (
            let x = -1000;
            x <= 1000;
            x += grid
        ) {
            const screen = worldToScreen(x, 0);

            ctx.beginPath();
            ctx.moveTo(screen.x, 0);
            ctx.lineTo(screen.x, window.innerHeight);
            ctx.stroke();
        }

        for (
            let y = -1000;
            y <= 1000;
            y += grid
        ) {
            const screen = worldToScreen(0, y);

            ctx.beginPath();
            ctx.moveTo(0, screen.y);
            ctx.lineTo(window.innerWidth, screen.y);
            ctx.stroke();
        }
    }

    function drawPlace(place) {
        const position = worldToScreen(place.x, place.y);

        ctx.fillStyle = "rgba(255,255,255,0.08)";
        ctx.fillRect(
            position.x - place.width / 2,
            position.y - place.height / 2,
            place.width,
            place.height
        );

        ctx.strokeStyle = "rgba(255,255,255,0.3)";
        ctx.strokeRect(
            position.x - place.width / 2,
            position.y - place.height / 2,
            place.width,
            place.height
        );

        ctx.fillStyle = "#fff";
        ctx.textAlign = "center";
        ctx.font = "bold 15px Century Schoolbook";

        ctx.fillText(
            place.title,
            position.x,
            position.y + 5
        );
    }

    function drawPlayer() {
        const x = window.innerWidth / 2;
        const y = window.innerHeight / 2;

        ctx.beginPath();
        ctx.arc(
            x,
            y,
            player.size,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = "#ffffff";
        ctx.fill();

        ctx.strokeStyle = "#000000";
        ctx.stroke();
    }

    function distanceToPlace(place) {
        const dx = player.x - place.x;
        const dy = player.y - place.y;

        return Math.sqrt(dx * dx + dy * dy);
    }

    function nearestPlace() {
        let nearest = null;
        let nearestDistance = Infinity;

        for (const place of places) {
            const distance = distanceToPlace(place);

            if (distance < nearestDistance) {
                nearest = place;
                nearestDistance = distance;
            }
        }

        return {
            place: nearest,
            distance: nearestDistance
        };
    }

    function interact() {
        const result = nearestPlace();

        if (!result.place || result.distance > 120) {
            return;
        }

        interactionTitle.textContent =
            result.place.title;

        interactionDescription.textContent =
            result.place.description;

        panel.classList.remove("hidden");
    }

    function draw() {
        drawBackground();

        for (const place of places) {
            drawPlace(place);
        }

        drawPlayer();

        const result = nearestPlace();

        if (result.place && result.distance <= 120) {
            status.textContent =
                `NEAR: ${result.place.title} — PRESS E`;
        } else {
            status.textContent =
                "MUKTI MAHAL — EXPLORE";
        }
    }

    function loop() {
        update();
        draw();
        requestAnimationFrame(loop);
    }

    window.addEventListener("resize", resize);

    window.addEventListener("keydown", event => {
        keys.add(event.key);

        if (
            event.key === "e" ||
            event.key === "E"
        ) {
            interact();
        }
    });

    window.addEventListener("keyup", event => {
        keys.delete(event.key);
    });

    closeInteraction.addEventListener(
        "click",
        () => {
            panel.classList.add("hidden");
        }
    );

    resize();
    loop();
})();
