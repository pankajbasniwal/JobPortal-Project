
async function loadJobs() {

    const container = document.getElementById("jobsList");

    try {

        const response = await fetch("/api/jobs/");
        const jobs = await response.json();

        container.innerHTML = "";

        if (!response.ok) {
            container.textContent = "Unable to load jobs.";
            return;
        }

        if (jobs.length === 0) {
            container.textContent = "No jobs available currently.";
            return;
        }

        jobs.forEach(job => {

            const card = document.createElement("div");
            card.className = "job-card";

            const title = document.createElement("h2");
            title.textContent = job.title;

            const location = document.createElement("p");
            location.textContent = "Location: " + job.location;

            const type = document.createElement("p");
            type.textContent = "Job Type: " + job.job_type;

            const salary = document.createElement("p");
            salary.textContent = "Salary: " +
                (job.salary || "Not specified");

            const skills = document.createElement("p");
            skills.textContent = "Skills: " + job.skills_required;

            const description = document.createElement("p");
            description.textContent = job.description;

            const applyLink = document.createElement("a");

            applyLink.href = `/apply/${job.id}/`;

            applyLink.textContent = "Apply Now";

            applyLink.className = "apply-btn";

            card.append(
                title,
                location,
                type,
                salary,
                skills,
                description,
                applyLink
            );

            container.appendChild(card);

        });

    } catch (error) {

        container.textContent = "Something went wrong.";

        console.log(error);

    }
}

loadJobs();
