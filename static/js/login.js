
document.getElementById("loginForm")
.addEventListener("submit", async function(event) {

    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const data = {
        username: username,
        password: password
    };

    try {

        const response = await fetch("/api/accounts/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        const message = document.getElementById("message");

        if (response.ok) {

            // Save login details in session storage
            sessionStorage.setItem("token", result.token);
            sessionStorage.setItem("username", result.username);
            sessionStorage.setItem("role", result.role);

            message.style.color = "green";
            message.innerText = "Login successful!";

            // Redirect according to user role
            if (result.role === "student") {
                window.location.href = "/student-dashboard/";
            } else {
                window.location.href = "/recruiter-dashboard/";
            }

        } else {

            message.style.color = "red";
            message.innerText = result.error || JSON.stringify(result);

        }

    } catch (error) {

        document.getElementById("message").innerText =
            "Something went wrong. Please try again.";

        console.log(error);

    }

});
