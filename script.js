document.addEventListener('DOMContentLoaded', function() {
    function fetchData() {
        fetch('/get_text') 
            .then(response => response.text())
            .then(data => {
                document.getElementById('output').textContent = data;
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    fetchData();
});
