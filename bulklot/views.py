from django.http import HttpResponse
from django.views import generic
from django.urls import reverse

from .models import LotRequest, LotRequestTime
from .forms import LotReqTimeFormSet

class LotReqList(generic.ListView):
    model = LotRequest

class LotReqDetail(generic.DetailView):
    model = LotRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lotreqtime_list'] = self.object.lotrequesttime_set.all()
        return context

class LotReqCreate(generic.CreateView):
    model = LotRequest
    fields = ['location']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['lotreqtime_formset'] = LotReqTimeFormSet(self.request.POST)
        else:
            context['lotreqtime_formset'] = LotReqTimeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        lotReqTimeFormSet = context['lotreqtime_formset'];
        if form.is_valid() and lotReqTimeFormSet.is_valid():
            self.object = form.save()
            lotReqTimeFormSet.instance = self.object
            lotReqTimeFormSet.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bulklot:lot_req_detail', kwargs={'pk': self.object.pk})

