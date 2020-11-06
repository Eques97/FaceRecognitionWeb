
var CameraWidth;
var CameraHeight;
var video;

function RequestMedia() {
    video = document.getElementById("video");
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
                var mediaTrackSettings = stream.getVideoTracks()[0].getSettings()
                CameraWidth = mediaTrackSettings.width;
                CameraHeight = mediaTrackSettings.height;
            })
            .catch(function (err0r) {
                console.log("Something went wrong!");
            });
    }
}

function Submit() {
    var canvas = document.getElementById("canvas");
    canvas.width = CameraWidth;
    canvas.height = CameraHeight;
    var context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, CameraWidth, CameraHeight);
    var dataURL = canvas.toDataURL("image/png");
    document.getElementById("image").value = dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

window.onload = RequestMedia;