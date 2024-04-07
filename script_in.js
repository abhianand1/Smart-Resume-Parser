document.addEventListener('DOMContentLoaded', function() {
    const page1 = document.getElementById('page1');
    const page2 = document.getElementById('page2');
    const page3 = document.getElementById('page3');
    const smartModeCheckbox = document.getElementById('smart-mode');
    const multiModeCheckbox = document.getElementById('multi-mode');
    const jobTitleInput = document.getElementById('job-title');
    const jobDescriptionInput = document.getElementById('job-description');
    const folderInput = document.getElementById('folder');
    const fileInput = document.getElementById('file');
    const submitPage1Btn = document.getElementById('submit-page1');
    const submitPage2Btn = document.getElementById('submit-page2');
    const submitPage3Btn = document.getElementById('submit-page3');

    submitPage1Btn.addEventListener('click', function() {
        page1.classList.remove('active');
        if (smartModeCheckbox.checked) {
            page2.classList.add('active');
        } else {
            page3.classList.add('active');
        }
    });

    submitPage2Btn.addEventListener('click', function() {
        page2.classList.remove('active');
        page3.classList.add('active');
    });

    submitPage3Btn.addEventListener('click', function() {
        const smartMode = smartModeCheckbox.checked ? 'yes' : 'no';
        const multiMode = multiModeCheckbox.checked ? 'yes' : 'no';
        const jobTitle = jobTitleInput.value.trim();
        const jobDescription = jobDescriptionInput.value.trim();
        const folderPath = folderInput.value ? folderInput.value.trim() : null;
        const filePath = fileInput.value ? fileInput.value.trim() : null;

        console.log('Smart Mode:', smartMode);
        console.log('Multi Mode:', multiMode);
        console.log('Job Title:', jobTitle);
        console.log('Job Description:', jobDescription);
        console.log('Folder Path:', folderPath);
        console.log('File Path:', filePath);
    });
});
