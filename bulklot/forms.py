from django.forms import ModelForm, inlineformset_factory, DateInput
from .models import LotRequest, LotRequestTime

LotReqTimeFormSet = inlineformset_factory(
    LotRequest,
    LotRequestTime,
    fields=['member', 'date', 'time'],
    can_delete=False,
    widgets={'date': DateInput(attrs={"type":"date"})},
    extra=2,
    min_num=1,
    validate_min=True,
    )

def lotReqTimeFormSet_factory(extra):
    return inlineformset_factory( 
        LotRequest, 
        LotRequestTime,
        fields=['member', 'date', 'time'],
        can_delete=False,
        widgets={'date': DateInput(attrs={"type":"date"})},
        extra=extra,
        min_num=1,
        validate_min=True,
        )
