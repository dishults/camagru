(function () {

    var width = 320;    // We will scale the photo width to this
    var height = width / (4 / 3);     // This will be computed based on the input stream

    var video = document.getElementById("video");
    var canvas = document.getElementById('canvas');
    var preview = canvas.getContext('2d');

    var snapshot = document.getElementById('snapshot');
    var upload = document.getElementById('id_image');
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
            })
            .catch(function (err) {
                document.getElementById('webcam').hidden = true;
                console.log("Couldn't get a stream: " + err);
            });
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
    }

    snapshot.addEventListener('click', function (e) {
        upload.value = '';
        preview.clearRect(0, 0, canvas.width, canvas.height);
        preview.drawImage(video, 0, 0, canvas.width, canvas.height);

        imageString.value = canvas.toDataURL('image/png');
    }, false);

    upload.addEventListener('change', function (e) {
        if (this.files && this.files[0]) {
            var image = new Image();
            image.onload = function () {
                height = image.height / (image.width / width);
                preview.clearRect(0, 0, canvas.width, canvas.height);
                preview.drawImage(image, 0, 0, width, height);
            }
            image.src = URL.createObjectURL(this.files[0]);;
            URL.revokeObjectURL(image.src);
        }
    });

})();