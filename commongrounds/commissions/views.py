from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission, CommissionType
from django.db.models import Case, Value, When, IntegerField


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions_list.html'
    context_object_name = "commissions"

    def get_queryset(self, *args, **kwargs):
        return Commission.objects.annotate(
            status_order=Case(
                When(status="open", then=Value(0)),
                When(status="full", then=Value(1)),
                When(status="completed", then=Value(2)),
                When(status="discontinued", then=Value(3)),
                output_field=IntegerField()
            )
        ).order_by('status_order', '-created_on')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            user_commissions = self.get_queryset().filter(maker= user.profile)

            applied_commissions = self.get_queryset().filter(jobs__jobapplications__applicant = user.profile)

            all_commissions = self.get_queryset().exclude(maker=user.profile)


            context['user_commissions'] = user_commissions
            context['applied_commissions'] = applied_commissions
            context['all_commissions'] = all_commissions
        else:
            context['all_commissions'] = self.get_queryset()

        return context
    
class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.get_object()    
        jobs = commission.jobs.all() 

        total_manpower = sum(job.manpower_required for job in jobs)

        accepted_counts = {
            job.id: job.jobapplications.filter(status="accepted").count()
            for job in jobs
        }
        open_manpower = sum(
            max(job.manpower_required - accepted_counts[job.id], 0)
            for job in jobs
        )
        context['is_owner'] = self.request.user == commission.maker.user
        context['total_manpower'] = total_manpower
        context['open_manpower'] = open_manpower

        user = self.request.user
        jobs_with_status = []
        for job in jobs:
            is_full = accepted_counts[job.id] >= job.manpower_required
            already_applied = (
                user.is_authenticated and
                job.jobapplications.filter(applicant=user.profile).exists()
            )
            jobs_with_status.append({
                'job': job,
                'is_full': is_full,
                'already_applied': already_applied,
            })

        return context
