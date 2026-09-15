/*
 * MUKTI MAHAL
 * REAL AI VIDEO CREATION
 */

const API_BASE =
    "https://rajeshkhandelwalofficial.onrender.com";

const promptInput =
    document.getElementById(
        "video-prompt"
    );

const modelInput =
    document.getElementById(
        "video-model"
    );

const secondsInput =
    document.getElementById(
        "video-seconds"
    );

const sizeInput =
    document.getElementById(
        "video-size"
    );

const createButton =
    document.getElementById(
        "create-video"
    );

const statusElement =
    document.getElementById(
        "creation-status"
    );

const resultCard =
    document.getElementById(
        "result-card"
    );

const resultProgress =
    document.getElementById(
        "result-progress"
    );

const generatedVideo =
    document.getElementById(
        "generated-video"
    );

const resultData =
    document.getElementById(
        "result-data"
    );


let currentVideoId =
    null;

let pollingTimer =
    null;


/* =========================================================
   STATUS
   ========================================================= */

function setStatus(message) {

    statusElement.textContent =
        message;
}


/* =========================================================
   CREATE VIDEO
   ========================================================= */

async function createVideo() {

    const prompt =
        promptInput.value.trim();

    if (!prompt) {

        setStatus(
            "PLEASE ENTER A VIDEO PROMPT"
        );

        promptInput.focus();

        return;
    }


    createButton.disabled =
        true;

    setStatus(
        "SENDING VIDEO REQUEST..."
    );


    resultCard.classList.remove(
        "hidden"
    );

    generatedVideo.classList.add(
        "hidden"
    );

    resultProgress.textContent =
        "CREATING VIDEO...";


    resultData.textContent =
        "";


    try {

        const response =
            await fetch(
                `${API_BASE}/mukti-mahal/creation/video`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            prompt,

                            model:
                                modelInput.value,

                            seconds:
                                secondsInput.value,

                            size:
                                sizeInput.value

                        })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Video creation request failed."
            );
        }


        currentVideoId =
            data.id;


        resultData.textContent =
            JSON.stringify(
                data,
                null,
                2
            );


        setStatus(
            "VIDEO GENERATION STARTED"
        );


        resultProgress.textContent =
            `STATUS: ${
                data.status || "PROCESSING"
            }`;


        if (currentVideoId) {

            startPolling(
                currentVideoId
            );

        } else {

            createButton.disabled =
                false;
        }


    } catch (error) {

        setStatus(
            "CREATION FAILED"
        );

        resultProgress.textContent =
            error.message;


        resultData.textContent =
            error.stack ||
            error.message;


        createButton.disabled =
            false;
    }
}


/* =========================================================
   POLLING
   ========================================================= */

function startPolling(
    videoId
) {

    stopPolling();


    pollingTimer =
        setInterval(
            () => {

                checkVideo(
                    videoId
                );

            },
            5000
        );


    checkVideo(
        videoId
    );
}


function stopPolling() {

    if (
        pollingTimer
    ) {

        clearInterval(
            pollingTimer
        );

        pollingTimer =
            null;
    }
}


/* =========================================================
   CHECK VIDEO
   ========================================================= */

async function checkVideo(
    videoId
) {

    try {

        const response =
            await fetch(
                `${API_BASE}/mukti-mahal/creation/video/${encodeURIComponent(videoId)}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to retrieve video status."
            );
        }


        resultData.textContent =
            JSON.stringify(
                data,
                null,
                2
            );


        const status =
            String(
                data.status ||
                ""
            ).toLowerCase();


        const progress =
            data.progress ??
            0;


        resultProgress.textContent =
            `STATUS: ${
                data.status || "PROCESSING"
            } — ${progress}%`;


        if (
            status === "completed"
        ) {

            stopPolling();

            setStatus(
                "VIDEO CREATED"
            );


            resultProgress.textContent =
                "VIDEO CREATED";


            createButton.disabled =
                false;


            /*
             * The API currently returns job metadata.
             * Once the provider download endpoint is
             * connected, the resulting MP4 URL will be
             * assigned here.
             */

            if (
                data.video_url
            ) {

                generatedVideo.src =
                    data.video_url;

                generatedVideo.classList.remove(
                    "hidden"
                );
            }

            return;
        }


        if (
            status === "failed"
        ) {

            stopPolling();

            setStatus(
                "VIDEO GENERATION FAILED"
            );


            resultProgress.textContent =
                data.error?.message ||
                "Video generation failed.";


            createButton.disabled =
                false;

            return;
        }


        setStatus(
            `GENERATING VIDEO — ${progress}%`
        );


    } catch (error) {

        stopPolling();

        setStatus(
            "STATUS CHECK FAILED"
        );

        resultProgress.textContent =
            error.message;

        createButton.disabled =
            false;
    }
}


/* =========================================================
   CREATE BUTTON
   ========================================================= */

createButton.addEventListener(
    "click",
    createVideo
);


/* =========================================================
   CLEANUP
   ========================================================= */

window.addEventListener(
    "beforeunload",
    () => {

        stopPolling();
    }
);
