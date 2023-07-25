function handleSearchUserFormSubmit(event) {
    event.preventDefault();

    const username = document.getElementById('search-user-input').value;
    const url = '/profile/' + username;

    // Make an AJAX request to the server-side existence check API
    fetch('/check-user-exists', {
        method: 'POST',
        body: JSON.stringify({ username: username }),
        headers: {
        'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
        if (data.exists) {
            window.location.href = url; // Redirect to the user's profile page
        } else {
            //alert('User does not exist'); // Display an error message
            // You can choose to keep the user on the same page or perform a different action here
            const errorElement = document.getElementById('search-user-error');
            errorElement.textContent = 'User does not exist'; // Display the error message
            errorElement.classList.add('search-user-error-show'); // Show the error message element
        }
        })
        .catch(error => {
        console.error('Error:', error);
        });
    }

document.getElementById('search-user-form').addEventListener('submit', handleSearchUserFormSubmit);
