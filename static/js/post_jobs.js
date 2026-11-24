document.getElementById("jobForm").addEventListener("submit", async function(event) {

    event.preventDefault();

    const token = sessionStorage.getItem("token");
    const role = sessionStorage.getItem("role");
    const message = document.getElementById("message");

    if (!token || role !== "recruiter") {
        message.textContent = "Please login with a recruiter account.";
        message.style.color = "red";
        return;
    }

    const jobData = {
        title: document.getElementById("title").value,
        description: document.getElementById("description").value,
        company_id :document.getElementById("company").value,
        skills_required: document.getElementById("skills_required").value,
        location: document.getElementById("location").value,
        salary: document.getElementById("salary").value || null,
        job_type: document.getElementById("job_type").value,
        deadline: document.getElementById("deadline").value || null
    };

    try {
        const response = await fetch("/api/jobs/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Token " + token
            },
            body: JSON.stringify(jobData)
        });

        const result = await response.json();

        if (response.ok) {
            message.style.color = "green";
            message.textContent = "Job posted successfully!";
            document.getElementById("jobForm").reset();
        } else {
            message.style.color = "red";
            message.textContent = JSON.stringify(result);
        }

    } catch (error) {
        message.textContent = "Something went wrong.";
        message.style.color = "red";
    }

});