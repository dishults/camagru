(function () {
    const width = 500;    // We will scale the photo width to this
    let height = width / (4 / 3);     // This will be computed based on the input stream

    const canvas = document.getElementById('canvas');
    const preview = canvas.getContext('2d');
    preview.image = null;
    window.location.hash = '';

    // **************** Snapshot ****************
    const video = document.getElementById("video");
    const snapshot = document.getElementById('snapshot');
    const imageString = document.getElementById('id_image_string');

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(stream => {
                video.srcObject = stream;
                height = video.videoHeight / (video.videoWidth / width);

                if (isNaN(height)) {
                    height = width / (4 / 3);
                }
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

        imageString.value = canvas.toDataURL('image/png');
        preview.image = new Image();
        preview.image.src = imageString.value;
        window.location.hash = '#overlays';
    }, false);

    // **************** Upload ****************
    const upload = document.getElementById('id_image');
    const uploadButton = document.getElementById('upload');
    uploadButton.disabled = true;

    upload.addEventListener('change', function (e) {
        if (this.files && this.files[0]) {
            clearImage();
            const image = new Image();
            image.onload = function () {
                height = image.height / (image.width / width);
                preview.drawImage(image, 0, 0, width, height);
                preview.image = image;
            }
            image.src = URL.createObjectURL(this.files[0]);;
            URL.revokeObjectURL(image.src);
            window.location.hash = '#overlays';
        }
    });

    // **************** Thumbnail ****************
    const thumbnails = document.getElementsByName('thumbnails');
    let selectedImage = 0;

    function loadImage() {
        clearImage(true);
        selectedImage = this.getAttribute('id');
        const imageThumb = this.children[0];
        const imageFull = new Image();
        imageFull.onload = function () {
            height = imageFull.height / (imageFull.width / width);
            preview.drawImage(imageFull, 0, 0, width, height);
            preview.image = imageFull;
        }
        imageFull.src = '/static/images/' + imageThumb.src.split('/').slice(-1)[0];
        window.location.hash = '#overlays';
    }

    thumbnails.forEach(item => {
        item.addEventListener('click', loadImage);
    });

    // **************** Overlay ****************
    const overlays = document.getElementsByName('overlays');
    let selectedOverlay = 0;

    function applyOverlay() {
        selectedOverlay = this.getAttribute('id');
        const image = this.children[0];
        if (preview.image) {
            preview.clearRect(0, 0, canvas.width, canvas.height);
            preview.drawImage(preview.image, 0, 0, width, height);
            preview.drawImage(image, 0, 0, width, height);
            uploadButton.disabled = false;
            window.location.hash = uploadButton.id;
        } else {
            alert("Take/upload/choose a picture first and then apply an overlay ;)");
        }
    }

    overlays.forEach(item => {
        item.addEventListener('click', applyOverlay);
    });

    // **************** Other ****************

    function clearImage(clearUpload) {
        preview.clearRect(0, 0, canvas.width, canvas.height);
        preview.image = null;
        window.location.hash = '';

        // snapshot
        imageString.value = '';

        // upload
        if (clearUpload) upload.value = '';
        uploadButton.disabled = true;

        // thumbnail
        selectedImage = 0;

        // overlay
        selectedOverlay = 0;
    }

    document.getElementById("upload_form").onsubmit = function () {
        imageString.value = `image:${selectedImage};overlay:${selectedOverlay};${imageString.value}`
    };
})();