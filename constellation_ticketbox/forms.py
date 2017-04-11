from .models import Box
from .models import Ticket
from django.forms import ModelForm


class BoxForm(ModelForm):
    """Form for the Box model"""
    def __init__(self, *args, **kwargs):
        super(BoxForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'mdl-textfield__input'
        self.fields['desc'].widget.attrs['class'] = 'mdl-textfield__input'
        self.fields['desc'].widget.attrs['rows'] = 3

    class Meta:
        model = Box
        fields = ['name', 'desc']


class TicketForm(ModelForm):
    """Form for the Ticket model"""
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['anonymous'].widget.attrs['class'] = 'mdl-switch__input'
        self.fields['title'].widget.attrs['class'] = 'mdl-textfield__input'
        self.fields['body'].widget.attrs['class'] = 'mdl-textfield__input'
        self.fields['body'].widget.attrs['rows'] = 3
        self.fields['status'].widget.attrs['class'] = 'mdl-textfield__input'

    class Meta:
        model = Ticket
        fields = ['title', 'body', 'anonymous', 'status']


class ReplyForm(ModelForm):
    """Form for the Reply model"""
    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['class'] = 'mdl-textfield__input'
        self.fields['body'].widget.attrs['rows'] = 3

    class Meta:
        model = Ticket
        fields = ['body']
