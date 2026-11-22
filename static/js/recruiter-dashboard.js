
const token = sessionStorage.getItem("token");
const role = sessionStorage.getItem("role");
const username = sessionStorage.getItem("username");

// Check recruiter login
if (!token || role !== "recruiter") {
    window.location.href = "/login/";
}

// Display username
document.getElementById("username").textContent = username;

// Get received applications
async function loadApplications() {

    try {

        const response = await fetch(
            "/api/applications/recruiter-applications/",
            {
                headers: {
                    "Authorization": "Token " + token
                }
            }
        );

        const data = await response.json();

        const container = document.getElementById("applications");

        container.innerHTML = "";

        if (!response.ok) {
            container.textContent = "Unable to load applications.";
            return;
        }

        if (data.length === 0) {
            container.textContent = "No applications received yet.";
            return;
        }

        data.forEach(app => {

            const card = document.createElement("div");
            card.className = "application-item";

            const title = document.createElement("h3");
            title.textContent = app.job_title;

            const student = document.createElement("p");
            student.textContent = "Student: " + app.student_name;

            const status = document.createElement("p");
            status.textContent = "Status: " + app.status;

            card.append(title, student, status);
            container.appendChild(card);

        });

    } catch (error) {

        document.getElementById("applications").textContent =
            "Something went wrong.";

        console.log(error);

    }
}

function logout() {
    sessionStorage.clear();
    window.location.href = "/login/";
}

loadApplications();
