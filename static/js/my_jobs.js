
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
                jobs.detail || jobs.error || "Unable to load your jobs.";
            return;
        }

        if (jobs.length === 0) {
            container.innerHTML = "You have not posted any jobs yet.";
            return;
        }

        // Clear old job cards
        container.innerHTML = "";

        // Display each job
        jobs.forEach(job => {
            container.innerHTML += `
                <div class="job-card">
                    <h2>${job.title}</h2>

                    <p><b>Location:</b> ${job.location}</p>
                    <p><b>Job Type:</b> ${job.job_type}</p>
                    <p><b>Salary:</b> ${job.salary || "Not specified"}</p>
                    <p>${job.description}</p>

                    <button onclick="editJob(${job.id})">
                        Edit Job
                    </button>

                    <button onclick="deleteJob(${job.id})">
                        Delete Job
                    </button>
                </div>
            `;
        });

    } catch (error) {
        container.innerHTML = "Server connection failed.";
        console.error(error);
    }
}


// EDIT JOB
async function editJob(id) {
    const title = prompt("Enter new job title:");

    if (!title || !title.trim()) {
        return;
    }

    try {
        const response = await fetch(`/api/jobs/${id}/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Token " + token
            },
            body: JSON.stringify({
                title: title.trim()
            })
        });

        const result = await response.json();

        if (response.ok) {
            alert("Job updated successfully!");
            loadMyJobs();
        } else {
            alert(JSON.stringify(result));
        }

    } catch (error) {
        alert("Unable to update job.");
        console.error(error);
    }
}


// DELETE JOB
async function deleteJob(id) {
    const confirmDelete = confirm(
        "Are you sure you want to delete this job?"
    );

    if (!confirmDelete) {
        return;
    }

    try {
        const response = await fetch(`/api/jobs/${id}/`, {
            method: "DELETE",
            headers: {
                "Authorization": "Token " + token
            }
        });

        if (response.ok) {
            alert("Job deleted successfully!");
            loadMyJobs();
        } else {
            const result = await response.json();
            alert(JSON.stringify(result));
        }

    } catch (error) {
        alert("Unable to delete job.");
        console.error(error);
    }
}


// Load jobs when page opens
loadMyJobs();
