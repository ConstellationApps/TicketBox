from .models import Box
from .models import Ticket
from django.forms import ModelForm


class BoxForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(BoxForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mdl-textfield__input'
            field.widget.attrs['rows'] = 3

    class Meta:
        model = Box
        fields = ['name', 'desc', 'archived']


class TicketForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mdl-textfield__input'
            field.widget.attrs['rows'] = 3

    class Meta:
        model = Ticket
        fields = ['title', 'body', 'anonymous', 'status', ]


class ReplyForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mdl-textfield__input'
            field.widget.attrs['rows'] = 3

    class Meta:
        model = Ticket
        fields = ['body']
