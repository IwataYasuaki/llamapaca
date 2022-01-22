import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import LotRequest, LotRequestTime, Member
from .forms import LotReqTimeFormSet, lotReqTimeFormSet_factory
from .utils import login_to_tmgbc

class Index(LoginRequiredMixin, generic.base.TemplateView):
    template_name = 'bulklot/index.html'

class LotReqList(LoginRequiredMixin, generic.ListView):
    model = LotRequest

    def get_queryset(self):
        return LotRequest.objects.filter(requester=self.request.user).order_by('-req_date')

class LotReqDetail(LoginRequiredMixin, generic.DetailView):
    model = LotRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lotreqtime_list'] = self.object.lotrequesttime_set.order_by('id')
        return context

class LotReqCreate(LoginRequiredMixin, generic.CreateView):
    model = LotRequest
    fields = ['sport', 'location']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['lotreqtime_formset'] = LotReqTimeFormSet(self.request.POST)
        else:
            initial = []
            members = Member.objects.filter(owner=self.request.user) 
            amonthago = datetime.date.today() + datetime.timedelta(days=31)
            date = datetime.date(amonthago.year, amonthago.month, 1)
            for member in members:
                initial += [{'member': member, 'date': date, 'time': '1300_1500'}]
                initial += [{'member': member, 'date': date, 'time': '1300_1500'}]
            lotReqTimeFormSet = lotReqTimeFormSet_factory(len(initial)-1)
            context['lotreqtime_formset'] = lotReqTimeFormSet(initial=initial)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        lotReqTimeFormSet = context['lotreqtime_formset'];

        if form.is_valid() and lotReqTimeFormSet.is_valid():
            form.instance.requester = self.request.user
            self.object = form.save()
            lotReqTimeFormSet.instance = self.object
            lotReqTimes = lotReqTimeFormSet.save()
    
            # フォームの入力値を取得
            sport = self.request.POST.get('sport')
            location = self.request.POST.get('location').split(',')
            location_page = location[0]
            location_id = location[1]
            for lotReqTime in lotReqTimes:
                print(lotReqTime.member, lotReqTime.member.tmgbc_id, lotReqTime.member.tmgbc_password)
                date = self.request.POST.get('lotrequesttime_set-0-date').replace('-0', '-').replace('-', ',')
                time = self.request.POST.get('lotrequesttime_set-0-time') 
                # 非同期で抽選申込を実行
                login_to_tmgbc.delay(lotReqTime, sport, location_page, location_id, date, time)
        else:
            return self.form_invalid(form)
    
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('bulklot:lot_req_detail', kwargs={'pk': self.object.pk})

class MemberList(LoginRequiredMixin, generic.ListView):
    model = Member

    def get_queryset(self):
        return Member.objects.filter(owner=self.request.user)

class MemberCreate(LoginRequiredMixin, generic.CreateView):
    model = Member
    fields = ['name', 'tmgbc_id', 'tmgbc_password']
    success_url = reverse_lazy('bulklot:member_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MemberUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Member
    fields = ['name', 'tmgbc_id', 'tmgbc_password']
    success_url = reverse_lazy('bulklot:member_list')

class MemberDelete(LoginRequiredMixin, generic.DeleteView):
    model = Member
    fields = ['name', 'tmgbc_id', 'tmgbc_password']
    success_url = reverse_lazy('bulklot:member_list')

