
const token = sessionStorage.getItem("token");

async function loadApplications() {

    const container = document.getElementById("applications-container");

    if (!token) {
        container.innerHTML = "Please login first.";
        return;
    }

    try {

        const response = await fetch(
            "/api/applications/recruiter-applications/",
            {
                method: "GET",
                headers: {
                    "Authorization": "Token " + token
                }
            }
        );

        const applications = await response.json();

        if (!response.ok) {
            container.innerHTML =
                applications.detail ||
                applications.error ||
                "Unable to load applications.";
            return;
        }

        if (applications.length === 0) {
            container.innerHTML = "No applications received yet.";
            return;
        }

        container.innerHTML = "";

        applications.forEach(app => {

            container.innerHTML += `
                <div class="job-card">

                    <h2>${app.student_name}</h2>

                    <p><b>Job:</b> ${app.job_title}</p>

                    <p><b>Company:</b> ${app.company_name}</p>

                    <p><b>Status:</b> ${app.status}</p>

                    <p><b>Applied Date:</b> ${new Date(app.applied_date).toLocaleDateString()}</p>

                </div>
            `;

        });

    } catch (error) {

        container.innerHTML = "Server connection failed.";
        console.error(error);

    }
}

loadApplications();
