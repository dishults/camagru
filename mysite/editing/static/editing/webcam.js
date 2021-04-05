(function () {

    var width = 500;    // We will scale the photo width to this
    var height = width / (4 / 3);     // This will be computed based on the input stream

    var video = document.getElementById("video");
    var canvas = document.getElementById('canvas');
    var preview = canvas.getContext('2d');

    var overlays = document.getElementsByName('overlays');
    var thumbnails = document.getElementsByName('thumbnails');
    var snapshot = document.getElementById('snapshot');
    var upload = document.getElementById('id_image');
    var imageString = document.getElementById('id_image_string');

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(stream => {
                video.srcObject = stream;
                height = video.videoHeight / (video.videoWidth / width);

                if (isNaN(height)) {
                    height = width / (4 / 3);
                }

                video.setAttribute('width', width);
                video.setAttribute('height', height);
            })
            .catch(err => {
                document.getElementById('webcam').hidden = true;
                console.log("Couldn't get a stream: " + err);
            });
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
    }

    snapshot.addEventListener('click', () => {
        upload.value = '';
        preview.clearRect(0, 0, canvas.width, canvas.height);
        preview.drawImage(video, 0, 0, canvas.width, canvas.height);

        imageString.value = canvas.toDataURL('image/png');
    }, false);

    upload.addEventListener('change', function (e) {
        if (this.files && this.files[0]) {
            imageString.value = '';
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

    function applyOverlay() {
        const image = this.children[0];
        preview.drawImage(image, 0, 0, width, height);
    }

    overlays.forEach(item => {
        item.addEventListener('click', applyOverlay);
    });

    function loadImage() {
        upload.value = '';
        const imageThumb = this.children[0];
        const imageFull = new Image();
        imageFull.src = '/static/images/' + imageThumb.src.split('/').slice(-1)[0];

        height = imageFull.height / (imageFull.width / width);
        preview.clearRect(0, 0, canvas.width, canvas.height);
        preview.drawImage(imageFull, 0, 0, width, height);
    }

    thumbnails.forEach(item => {
        item.addEventListener('click', loadImage);
    });

})();