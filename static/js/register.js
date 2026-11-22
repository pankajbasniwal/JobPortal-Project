
const role = document.getElementById("role");

const studentFields = document.getElementById("studentFields");
const recruiterFields = document.getElementById("recruiterFields");

// Show fields according to selected role
role.addEventListener("change", function () {

    if (role.value === "student") {
        studentFields.style.display = "block";
        recruiterFields.style.display = "none";
    } else {
        studentFields.style.display = "none";
        recruiterFields.style.display = "block";
    }

});

// Registration form submission
document.getElementById("registerForm")
.addEventListener("submit", async function(event) {

    event.preventDefault();

    const selectedRole = role.value;

    const data = {
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        role: selectedRole
    };

    if (selectedRole === "student") {

        data.phone = document.getElementById("phone").value;
        data.education = document.getElementById("education").value;
        data.skills = document.getElementById("skills").value;

    } else {

        data.company_name = document.getElementById("company_name").value;
        data.description = document.getElementById("description").value;
        data.website = document.getElementById("website").value;
        data.location = document.getElementById("location").value;

    }

    try {

        const response = await fetch(
            "/api/accounts/register/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        const result = await response.json();

        const message = document.getElementById("message");

        if (response.ok) {

            message.style.color = "green";
            message.innerText = "Registration successful! Please login.";

            document.getElementById("registerForm").reset();

            studentFields.style.display = "block";
            recruiterFields.style.display = "none";

        } else {

            message.style.color = "red";
            message.innerText = JSON.stringify(result);

        }

    } catch (error) {

        document.getElementById("message").innerText =
            "Something went wrong. Please try again.";

        console.log(error);

    }

});
