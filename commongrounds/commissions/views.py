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

            applied_commissions = self.get_queryset().filter(jobs__jobapplications__jobapplications_profile = user.profile)

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
