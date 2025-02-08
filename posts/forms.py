from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import Select

from .models import Post, Comment, Report
from .choices import REASON_CHOICES, FOOD_TYPE_CHOICES, TIPS_SITUATION_CHOICES, JOB_TYPE_CHOICES


class PostForm(forms.ModelForm):
    restaurant_name = forms.CharField(required=True)
    address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    date = forms.DateField(
        localize=False,
        input_formats=['%m/%Y'],
    )
    food_type = forms.ChoiceField(
        choices=[('', 'Cuisine Type')] + list(FOOD_TYPE_CHOICES),
        required=True,
    )
    tips_situation = forms.ChoiceField(
        choices=[('', 'Tipping Policy')] + list(TIPS_SITUATION_CHOICES),
        required=True
    )
    job_type = forms.ChoiceField(
        choices=[('', 'Position Type')] + list(JOB_TYPE_CHOICES),
        required=True
    )

    content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 10})
    )

    class Meta:
        model = Post
        fields = ["restaurant_name", "address", "tips_situation", "tips_sit_detail",
                  "food_type", "job_type", "date", "content"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PostForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.initial['date'] = self.instance.date.strftime('%m/%Y')
            self.fields["address"].widget.attrs["readonly"] = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "parent"]
        labels = {
            "content": _(''),
        }


class ReportForm(forms.ModelForm):
    reason = forms.ChoiceField(
        choices=[('', 'Reason for reporting')] + REASON_CHOICES,
        widget=Select(attrs={'class': 'report-selection'})
    )
    detail = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Optional: Add any relevant details about why you are reporting',
            'class': 'report-content',
        })
    )

    class Meta:
        model = Report
        fields = ['reason', 'detail']
