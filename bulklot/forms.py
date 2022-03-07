from django.forms import inlineformset_factory, DateInput
from .models import LotRequest, LotRequestTime

def lotReqTimeFormSet_factory(extra=0):
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
