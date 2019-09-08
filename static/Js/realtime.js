const POST_FREQUENCY = 5000;

const videoPlayer = document.querySelector("#player");
const captureButton = document.querySelector("#capture-btn");

const startMedia = () => {
    if (!("mediaDevices" in navigator)) {
        navigator.mediaDevices = {};
    }

    if (!("getUserMedia" in navigator.mediaDevices)) {
        navigator.mediaDevices.getUserMedia = constraints => {
            const getUserMedia =
                navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

            if (!getUserMedia) {
                return Promise.reject(new Error("getUserMedia is not supported"));
            } else {
                return new Promise((resolve, reject) =>
                    getUserMedia.call(navigator, constraints, resolve, reject)
                );
            }
        };
    }

    navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(stream => {
            videoPlayer.srcObject = stream;
            videoPlayer.style.display = "block";
        })
        .catch(err => {
            imagePickerArea.style.display = "block";
        });
};

function takepicture() {
    // create canvas
    var canvas = document.createElement('canvas');
    canvas.width = 500;
    canvas.height = 400;
    
    // get canvas context
    var context = canvas.getContext('2d');

    // if canvas has size (obviously it does)
    context.drawImage(videoPlayer, 0, 0, canvas.width, canvas.height);

    // get base64 image
    let picture = canvas.toDataURL();

    $.post("/realtime", {
        "photo": picture
    }).then((data, status) => {
        if (status == 200) {
            console.log("Successfully posted photo to backend")
        }

        // use data returned to post realtime updates to user
        var feedback_element = document.getElementById('feedback');

        if (feedback) {
            feedback_element.innerHTML = data['feedback'];
        }
    })
}

setInterval(function() {
    takepicture()
}, POST_FREQUENCY);

window.addEventListener("load", event => startMedia());