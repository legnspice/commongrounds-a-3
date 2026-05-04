from django.shortcuts import render, redirect
from accounts.decorators import role_required
from .forms import CommissionForm, JobFormSet
from .models import Commission, Job
from django.db.models import Case, Value, When, IntegerField, Q
from .services import CommissionService

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

        user_commissions = Commission.objects.filter(maker = profile).annotate(status_order=status_order).order_by('status_order', '-created_on').distinct()
        applied_commissions = Commission.objects.filter(jobs__jobapplications__applicant = profile).annotate(status_order=status_order).order_by('status_order', '-created_on').distinct()

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
    summary = CommissionService.get_commission_summary(commission)

    if request.user.is_authenticated:
        for entry in summary['jobs_with_status']:
            entry['already_applied'] = entry['job'].jobapplications.filter(
                applicant=request.user.profile
            ).exists()
    else:
        for entry in summary['jobs_with_status']:
            entry['already_applied'] = False
    
    context = {
        "commission": commission,
        "is_owner": request.user.is_authenticated and request.user == commission.maker.user,
        "total_manpower": summary['total_manpower'],
        "open_manpower": summary['open_manpower'],
        "jobs_with_status": summary['jobs_with_status'],
    }

    return render(request, "commissions_detail.html", context)

@role_required('Commission Maker')
def CommissionCreateView(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = CommissionForm(request.POST)
        formset = JobFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            data = form.cleaned_data
            jobs_data = [
                job_form.cleaned_data
                for job_form in formset
                if job_form.cleaned_data and not job_form.cleaned_data.get('DELETE')
            ]
            commission = CommissionService.create_commission(
                author=request.user.profile,
                data=data,
                jobs_data=jobs_data
            )
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

@role_required('Commission Maker')
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
            CommissionService.get_commission_summary(commission)
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

def JobApplicationCreateView(request, job_pk):
    if not request.user.is_authenticated:
        return redirect('login')

    job = Job.objects.get(pk=job_pk)

    if request.method == 'POST':
            CommissionService.apply_to_job(
                applicant=request.user.profile,
                job=job
            )
            return redirect(job.commission)

    context = {'job': job}
    return render(request, "jobapplication_form.html", context)