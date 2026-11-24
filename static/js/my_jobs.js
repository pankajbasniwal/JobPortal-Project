
const token = sessionStorage.getItem("token");

async function loadMyJobs() {
    const container = document.getElementById("jobs-container");

    if (!token) {
        container.innerHTML = "Please login first.";
        return;
    }

    try {
        const response = await fetch("/api/my-jobs/", {
            method: "GET",
            headers: {
                "Authorization": "Token " + token
            }
        });

        const jobs = await response.json();

        if (!response.ok) {
            container.innerHTML =
                jobs.detail || "Unable to load your jobs.";
            return;
        }

        if (jobs.length === 0) {
            container.innerHTML = "You have not posted any jobs yet.";
            return;
        }

        container.innerHTML = "";

        jobs.forEach(job => {
            container.innerHTML += `
                <div class="job-card">
                    <h2>${job.title}</h2>
                    <p><b>Location:</b> ${job.location}</p>
                    <p><b>Job Type:</b> ${job.job_type}</p>
                    <p><b>Salary:</b> ${job.salary || "Not specified"}</p>
                    <p>${job.description}</p>
                </div>
            `;
        });

    } catch (error) {
        container.innerHTML = "Server connection failed.";
        console.error(error);
    }
}

loadMyJobs();
