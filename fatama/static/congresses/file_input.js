const fileInputFields = document.querySelectorAll('.file.has-name');

fileInputFields.forEach((fileInputField) => {
    const fileInput = fileInputField.querySelector('.file-input');
    const fileName = fileInputField.querySelector('.file-name');

    fileInput.onchange = () => {
        if (fileInput.files.length > 0) {
            fileName.textContent = fileInput.files[0].name;
        }
    }
})
