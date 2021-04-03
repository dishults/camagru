(function () {

    var width = 320;    // We will scale the photo width to this
    var height = 0;     // This will be computed based on the input stream

    var video = document.getElementById("video");
    var canvas = document.getElementById('canvas');
    var cameraButton = document.getElementById('camera_button');
    var imageString = document.getElementById('id_image_string');

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(function (stream) {
                video.srcObject = stream;
                height = video.videoHeight / (video.videoWidth / width);

                if (isNaN(height)) {
                    height = width / (4 / 3);
                }

                video.setAttribute('width', width);
                video.setAttribute('height', height);
                canvas.setAttribute('width', width);
                canvas.setAttribute('height', height);
            })
            .catch(function (err) {
                document.getElementById('webcam').hidden = true;
                console.log("Couldn't get a stream: " + err);
            });
    }

    cameraButton.addEventListener('click', function (ev) {
        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, width, height);

        imageString.value = canvas.toDataURL('image/png');
    }, false);
})();