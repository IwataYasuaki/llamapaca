from django.forms import ModelForm, inlineformset_factory, DateInput
from .models import LotRequest, LotRequestTime

LotReqTimeFormSet = inlineformset_factory(
    LotRequest,
    LotRequestTime,
    fields=['date', 'time'],
    can_delete=False,
    widgets={'date': DateInput(attrs={"type":"date"})})

