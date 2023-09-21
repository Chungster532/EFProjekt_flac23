const toggleBtn = document.getElementsByClassName('toggle-btn')[0]
const navbarLinks = document.getElementsByClassName('header-right')[0]

toggleBtn.addEventListener('click', () => {
    navbarLinks.classList.toggle('active')
})
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const existingForm = document.getElementById('existing-form');

// Prevent default behavior to open file on drop
dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('highlight');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('highlight');
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('highlight');

    const files = e.dataTransfer.files;
    fileInput.files = files; // Assign the dropped files to the file input
});

// Handle file selection on click
dropArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    // No need to display files in a list, just leave the file input as it is
});

existingForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Send the form data to the server using a fetch request
    try {
        const formData = new FormData(existingForm);
        formData.append('username', 'example_user');

        const response = await fetch('/process', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            // Handle a successful response from the server
            console.log('Form submission successful');
        } else {
            // Handle an error response from the server
            console.error('Form submission failed');
        }
    } catch (error) {
        // Handle a network error
        console.error('Network error:', error);
    }
});