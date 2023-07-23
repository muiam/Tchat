    function submitLoginForm(event) {
        event.preventDefault(); // Prevent default form submission

        // Get the form data
        var username = document.getElementById("username").value;
        var password = document.getElementById("password").value;
        var csrfmiddlewaretoken= document.querySelector("input[name=csrfmiddlewaretoken]").value;


        // Create a data object to hold the form data
        var formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);
        formData.append("csrfmiddlewaretoken", csrfmiddlewaretoken);

        // Send the form data to the Django view using an AJAX request
        console.log("Form Data:");
        console.log("Username:", username);
        console.log("Password:", password);

        fetch("login/", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {

            if (data.user === '0') {
                console.log("Login failed: Invalid username or password");
                // Clear the login status if login is unsuccessful
                localStorage.removeItem('loggedIn');
            } else {
                // Set the login status in localStorage
                localStorage.setItem('loggedIn', 'true');
                // Hide the login form and display the logout button
                window.location.href = "";
            }
        })
        .catch(error => {
            // Handle any errors that occurred during the AJAX request
            console.log("Error:", error);
        });
    }


    function incrementPostViewCount() {
        const postsViewedToday = parseInt(localStorage.getItem("postsViewedToday")) || 0;
        localStorage.setItem("postsViewedToday", postsViewedToday + 1);
    
        // Log the updated value to the console
        console.log("Updated postsViewedToday:", postsViewedToday + 1);
    }
    

function SubmitPost(){
    alert('hi Bret, You just made a post 😍😍');
        window.location.href='myposts';
   
}




function showLinks() {
    // Get the links by their IDs
    const myfeedLink = document.getElementById('myfeed');
    const mypostsLink = document.getElementById('myposts');
    const profileLink = document.getElementById('profile');
    const logoutButton = document.getElementById('logoutbutton');
    const loginButton = document.getElementById('loginbutton');
    const commentbtn = document.getElementById('commentbtn');

    // Show the links and hide the login button
    myfeedLink.style.display = 'none';
    mypostsLink.style.display = 'none';

    profileLink.style.display = 'none';
    logoutButton.style.display = 'none';
    loginButton.style.display = 'inline-block';
    commentbtn.style.display='inline-block';
}

function showLogoutButton() {
    // Get the links by their IDs
    const myfeedLink = document.getElementById('myfeed');
    const mypostsLink = document.getElementById('myposts');
    const profileLink = document.getElementById('profile');
    const logoutButton = document.getElementById('logoutbutton');
    const loginButton = document.getElementById('loginbutton');
    const commentbtn = document.getElementById('commentbtn');

    // Hide the links and show the logout button
    myfeedLink.style.display = 'inline-block';
    mypostsLink.style.display = 'inline-block';
    profileLink.style.display = 'inline-block';
    logoutButton.style.display = 'inline-block';
    loginButton.style.display = 'none';
    commentbtn.style.display='inline-block';
    
}

function logout() {
   
    localStorage.setItem('loggedIn', 'false');
    showLinks();
    
}

window.addEventListener('load', function () {
    if (localStorage.getItem('loggedIn') === 'true') {
        showLogoutButton();
    } else {
        const postsViewedToday = parseInt(localStorage.getItem("postsViewedToday")) || 0;
        if(postsViewedToday >= 20){
            const confirmed = confirm(
                "You have exceeded your maximum daily limit. Would you like to log in or subscribe to view more?"
              );
            
              if (confirmed) {
                const loginModal = new bootstrap.Modal(document.getElementById("loginModal"));
                loginModal.show();
              }
        }

        showLinks();
        
    }
});

function trackView(){
    incrementPostViewCount();
}
