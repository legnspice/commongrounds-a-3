from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission, CommissionType

class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions_list.html'


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions_detail.html'