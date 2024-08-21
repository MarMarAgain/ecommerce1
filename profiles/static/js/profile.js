document.addEventListener('DOMContentLoaded', function () {
    const fileUpload = document.getElementById('id_profile_picture');
    const profilePhoto = document.getElementById('profile-photo');
    const label = document.querySelector('.profile-picture-label');

    // Function to update profile photo preview
    fileUpload.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                profilePhoto.src = e.target.result;
                label.textContent = 'File selected: ' + file.name;
            };
            reader.readAsDataURL(file);
        } else {
            label.textContent = 'Change profile picture';
        }
    });
});

