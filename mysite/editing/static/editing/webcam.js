(function () {

    var width = 500;    // We will scale the photo width to this
    var height = width / (4 / 3);     // This will be computed based on the input stream

    var canvas = document.getElementById('canvas');
    var preview = canvas.getContext('2d');
    preview.empty = true;

    // **************** Snapshot ****************
    var video = document.getElementById("video");
    var snapshot = document.getElementById('snapshot');
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
        clearImage(true);
        preview.drawImage(video, 0, 0, canvas.width, canvas.height);
        preview.empty = false;

        imageString.value = canvas.toDataURL('image/png');
    }, false);

    // **************** Upload ****************
    var upload = document.getElementById('id_image');
    var uploadButton = document.getElementById('upload');
    uploadButton.disabled = true;

    upload.addEventListener('change', function (e) {
        if (this.files && this.files[0]) {
            clearImage(false);
            var image = new Image();
            image.onload = function () {
                height = image.height / (image.width / width);
                preview.drawImage(image, 0, 0, width, height);
                preview.empty = false;
            }
            image.src = URL.createObjectURL(this.files[0]);;
            URL.revokeObjectURL(image.src);
        }
    });

    // **************** Thumbnail ****************
    var thumbnails = document.getElementsByName('thumbnails');
    var selectedImage = 0;

    function loadImage() {
        clearImage(true);
        selectedImage = this.getAttribute('id');
        const imageThumb = this.children[0];
        const imageFull = new Image();
        imageFull.src = '/static/images/' + imageThumb.src.split('/').slice(-1)[0];

        height = imageFull.height / (imageFull.width / width);
        preview.drawImage(imageFull, 0, 0, width, height);
        preview.empty = false;
    }

    thumbnails.forEach(item => {
        item.addEventListener('click', loadImage);
    });

    // **************** Overlay ****************
    var overlays = document.getElementsByName('overlays');
    var selectedOverlays = new Set([0]);

    function applyOverlay() {
        selectedOverlays.add(this.getAttribute('id'));
        const image = this.children[0];
        if (!preview.empty) uploadButton.disabled = false;
        preview.drawImage(image, 0, 0, width, height);
    }

    overlays.forEach(item => {
        item.addEventListener('click', applyOverlay);
    });

    // **************** Other ****************
    function clearImage(clearUpload) {
        if (clearUpload) upload.value = '';
        selectedImage = 0;
        imageString.value = '';
        selectedOverlays.clear();
        selectedOverlays.add(0);
        preview.clearRect(0, 0, canvas.width, canvas.height);
        preview.empty = true;
        uploadButton.disabled = true;
    }

    document.getElementById("upload_form").onsubmit = function () {
        imageString.value = `image:${selectedImage};overlays:${Array.from(selectedOverlays)};${imageString.value}`
    };

})();