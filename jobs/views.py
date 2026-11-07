from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import JobSeekerProfile

from .decorators import jobseeker_required, recruiter_required
from .forms import ApplicationForm, JobForm
from .matching import match
from .models import Application, Job


# ---------- Step 5: job posting (recruiters) ----------

@recruiter_required
def job_create(request):
    form = JobForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.instance.recruiter = request.user
        job = form.save()
        messages.success(request, f'Posted "{job.title}".')
        return redirect('my_jobs')
    return render(request, 'jobs/job_form.html', {'form': form})


@recruiter_required
def my_jobs(request):
    jobs = request.user.jobs.prefetch_related('skills', 'applications')
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


# ---------- Step 6: search and apply (job seekers) ----------

@login_required
def job_search(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')

    jobs = Job.objects.filter(is_open=True).prefetch_related('skills')
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(skills__name__icontains=query)
            | Q(recruiter__recruiter_profile__company_name__icontains=query)
        ).distinct()
    if category:
        jobs = jobs.filter(category=category)

    my_skills, applied_ids = [], set()
    if request.user.is_jobseeker and request.user.has_profile():
        my_skills = request.user.jobseeker_profile.skill_names()
        applied_ids = set(request.user.applications.values_list('job_id', flat=True))

    results = []
    for job in jobs:
        result = match(job.skill_names(), my_skills)
        result['job'] = job
        result['applied'] = job.id in applied_ids
        results.append(result)

    return render(request, 'jobs/search.html', {
        'results': results,
        'query': query,
        'category': category,
        'categories': Job.CATEGORY_CHOICES,
        'show_match': bool(my_skills),
    })


@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    context = {'job': job}
    if request.user.is_jobseeker and request.user.has_profile():
        context['result'] = match(job.skill_names(), request.user.jobseeker_profile.skill_names())
        context['already_applied'] = job.applications.filter(applicant=request.user).exists()
        context['form'] = ApplicationForm()
    return render(request, 'jobs/job_detail.html', context)


@jobseeker_required
@require_POST
def job_apply(request, pk):
    job = get_object_or_404(Job, pk=pk, is_open=True)
    if job.applications.filter(applicant=request.user).exists():
        messages.info(request, 'You have already applied to this job.')
        return redirect('job_detail', pk=pk)

    form = ApplicationForm(request.POST)
    if form.is_valid():
        form.instance.job = job
        form.instance.applicant = request.user
        form.save()
        messages.success(request, f'Applied to "{job.title}".')
    return redirect('job_detail', pk=pk)


@jobseeker_required
def my_applications(request):
    applications = request.user.applications.select_related('job')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


# ---------- Step 7: skill-matching dashboard (both) ----------

@login_required
def dashboard(request):
    if not request.user.has_profile():
        messages.info(request, 'Create your profile to see your skill matches.')
        return redirect('profile')
    if request.user.is_recruiter:
        return recruiter_dashboard(request)
    return jobseeker_dashboard(request)


def jobseeker_dashboard(request):
    """Open jobs that share at least one skill, best match first."""
    profile = request.user.jobseeker_profile
    my_skills = profile.skill_names()
    applied_ids = set(request.user.applications.values_list('job_id', flat=True))

    matches = []
    for job in Job.objects.filter(is_open=True).prefetch_related('skills'):
        result = match(job.skill_names(), my_skills)
        if result['matched']:
            result['job'] = job
            result['applied'] = job.id in applied_ids
            matches.append(result)
    matches.sort(key=lambda m: m['percent'], reverse=True)

    return render(request, 'jobs/dashboard_jobseeker.html', {'profile': profile, 'matches': matches})


def recruiter_dashboard(request):
    """For each of the recruiter's jobs, job seekers ranked by skill match."""
    seekers = JobSeekerProfile.objects.select_related('user').prefetch_related('skills')

    rows = []
    for job in request.user.jobs.prefetch_related('skills'):
        required = job.skill_names()
        applicant_ids = set(job.applications.values_list('applicant_id', flat=True))
        candidates = []
        for seeker in seekers:
            result = match(required, seeker.skill_names())
            applied = seeker.user_id in applicant_ids
            if result['matched'] or applied:
                result['seeker'] = seeker
                result['applied'] = applied
                candidates.append(result)
        candidates.sort(key=lambda c: c['percent'], reverse=True)
        rows.append({'job': job, 'candidates': candidates, 'applicant_count': len(applicant_ids)})

    return render(request, 'jobs/dashboard_recruiter.html', {'rows': rows})