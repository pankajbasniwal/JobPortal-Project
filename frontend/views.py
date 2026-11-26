from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def recruiter_dashboard(request):
    return render(request, 'recruiter_dashboard.html')

def jobs_page(request):
    return render(request, 'jobs.html')

def post_job_page(request):
    return render(request, 'post_job.html')

def apply_page(request, job_id):
    return render(request, 'apply.html', {
        'job_id': job_id
    })

def recruiter_applications_page(request):
    return render(request, 'recruiter_applications.html')

