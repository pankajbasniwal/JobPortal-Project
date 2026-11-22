
const applyForm = document.getElementById("applyForm");

applyForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const token = sessionStorage.getItem("token");
    const role = sessionStorage.getItem("role");

    const message = document.getElementById("message");
    const resume = document.getElementById("resume").files[0];

    // Check login
    if (!token) {
        message.style.color = "red";
        message.textContent = "Please login before applying.";
        return;
    }

    // Only students can apply
    if (role !== "student") {
        message.style.color = "red";
        message.textContent = "Only students can apply for jobs.";
        return;
    }

    // Check resume
    if (!resume || resume.type !== "application/pdf") {
        message.style.color = "red";
        message.textContent = "Please select a PDF resume.";
        return;
    }

    const jobId = applyForm.dataset.jobId;

    // Create FormData for file upload
    const formData = new FormData();
    formData.append("resume", resume);

    try {

        const response = await fetch(
            `/api/applications/apply/${jobId}/`,
            {
                method: "POST",
                headers: {
                    "Authorization": "Token " + token
                },
                body: formData
            }
        );

        const result = await response.json();

        if (response.ok) {

            message.style.color = "green";
            message.textContent =
                "Application submitted successfully!";

            applyForm.reset();

        } else {

            message.style.color = "red";
            message.textContent =
                result.error || JSON.stringify(result);

        }

    } catch (error) {

        message.style.color = "red";
        message.textContent = "Something went wrong.";

        console.log(error);

    }

});
