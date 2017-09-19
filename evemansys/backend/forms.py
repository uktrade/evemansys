from ckeditor.widgets import CKEditorWidget
from datetimewidget.widgets import DateWidget, TimeWidget
from django import forms

DATE_INPUT_FORMAT = ['%Y-%m-%d',
                     '%m/%d/%Y',
                     '%m/%d/%y',
                     '%d/%m/%Y',
                     ]

TIME_INPUT_FORMAT = ['%H:%M:%S']


class CreateEventForm1(forms.Form):
    date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=4),
                           input_formats=DATE_INPUT_FORMAT, help_text="Event date")
    start_time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=4),
                                 input_formats=TIME_INPUT_FORMAT, help_text="Start time")
    end_time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=4),
                               input_formats=TIME_INPUT_FORMAT, help_text="End time")


class CreateEventForm2(forms.Form):
    address = forms.CharField(widget=forms.Textarea)
    country = forms.CharField(max_length=100)
    postcode = forms.CharField(max_length=20)

    latitude = forms.DecimalField(help_text='Optional', required=False)
    longitude = forms.DecimalField(help_text='Optional', required=False)


class CreateEventForm3(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=CKEditorWidget())
