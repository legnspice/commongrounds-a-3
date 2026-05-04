from django.shortcuts import render, redirect
from accounts.decorators import role_required
from .forms import CommissionForm, JobFormSet
from .models import Commission
from django.db.models import Case, Value, When, IntegerField, Q

def CommissionListView(request):
    status_order = Case(
        When(status="open", then=Value(0)),
        When(status="full", then=Value(1)),
        When(status="completed", then=Value(2)),
        When(status="discontinued", then=Value(3)),
        output_field=IntegerField()
    )
    context = {}
    if request.user.is_authenticated:
        profile = request.user.profile

        user_commissions = Commission.objects.filter(maker = profile).annotate(status_order=status_order).order_by('status_order', '-created_on')
        applied_commissions = Commission.objects.filter(jobs__jobapplications__applicant = profile).annotate(status_order=status_order).order_by('status_order', '-created_on')

        all_commissions = Commission.objects.exclude(Q(maker = profile)|Q(jobs__jobapplications__applicant = profile)).distinct().annotate(status_order=status_order).order_by('status_order', '-created_on')

        context = {
            "user_commissions": user_commissions,
            "applied_commissions": applied_commissions,
            "all_commissions": all_commissions
        }

    else:
        all_commissions = Commission.objects.all().annotate(status_order=status_order).order_by('status_order', '-created_on')

        context = {
            "all_commissions": all_commissions
        }
    return render(request, "commissions_list.html", context)

def CommissionDetailView(request, pk):
    context = {}
    commission = Commission.objects.get(pk=pk)
    jobs = commission.jobs.all() 

    is_owner = request.user.is_authenticated and request.user == commission.maker.user
    total_manpower = sum(job.manpower_required for job in jobs)
    accepted_counts = sum(job.jobapplications.filter(status="accepted").count() for job in jobs)
    open_manpower = total_manpower - accepted_counts

    jobs_with_status = []
    for job in jobs:
        job_accepted = job.jobapplications.filter(status="accepted").count()
        is_full = job_accepted >= job.manpower_required
        already_applied = (
            request.user.is_authenticated and
            job.jobapplications.filter(applicant=request.user.profile).exists()
        )
        jobs_with_status.append({
            'job': job,
            'job_accepted':job_accepted,
            'is_full': is_full,
            'already_applied': already_applied,
        })

    context = {
        "commission": commission,
        "is_owner": is_owner,
        "total_manpower": total_manpower,
        "open_manpower": open_manpower,
        "jobs_with_status": jobs_with_status
    }

    return render(request, "commissions_detail.html", context)

def CommissionCreateView(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = CommissionForm(request.POST)
        formset = JobFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            commission = form.save(commit=False)
            commission.maker = request.user.profile
            commission.save()
            formset.instance = commission 
            formset.save()
            return redirect(commission)
    else:
        form = CommissionForm()
        formset = JobFormSet()

    context = {
        'form': form,
        'formset': formset,
        'heading': "Create a Commission"
    }
    return render(request, "commissions_form.html", context)

def CommissionUpdateView(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    commission = Commission.objects.get(pk=pk)

    if request.method == 'POST':
        form = CommissionForm(request.POST, instance=commission)
        formset = JobFormSet(request.POST, instance=commission)
        if form.is_valid() and formset.is_valid():
            commission = form.save(commit=False)
            jobs = commission.jobs.all()
            if jobs.exists() and all(job.status == "full" for job in jobs):
                commission.status = "full"
            commission.save()
            formset.save()
            return redirect(commission)
    else:
        form = CommissionForm(instance=commission)
        formset = JobFormSet(instance=commission)

    context = {
        'form': form,
        'formset': formset,
        'heading': "Edit Commission: " + commission.title
    }
    return render(request, "commissions_form.html", context)