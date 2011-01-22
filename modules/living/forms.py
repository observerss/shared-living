from django import forms
from django.contrib.auth.models import User

class CreateNewRecordForm(forms.Form):
    creater_name = forms.CharField(required=False,max_length=30)
    subject = forms.CharField(max_length=80)
    message = forms.CharField(required=False,widget=forms.Textarea,max_length=65536)
    amount = forms.FloatField()
    payer_names = forms.CharField(max_length=65536)
    consumer_names = forms.CharField(max_length=65536)
    tags = forms.CharField(max_length=100)
    spent_on = forms.DateField()
    
    # amount should be non-zero
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount<0:
            raise forms.ValidationError("Negative value not allowed!")
        if abs(amount)<0.01:
            raise forms.ValidationError("Amount should be>0.01!")
        return amount

    # make sure that payer's name is a valid username
    def clean_payer_names(self):
        payer_names = self.cleaned_data['payer_names'].split(',')
        for username in payer_names:
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    raise forms.ValidationError("You have entered inactive username!")
            except User.DoesNotExist:
                raise forms.ValidationError("You have entered invalid username!")
        return self.cleaned_data['payer_names']

    # make sure that consumer's name is a valid username
    def clean_consumer_names(self):
        consumer_names = self.cleaned_data['consumer_names'].split(',')
        for username in consumer_names:
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    raise forms.ValidationError("You have entered inactive username!")
            except User.DoesNotExist:
                raise forms.ValidationError("You have entered invalid username!")
        return self.cleaned_data['consumer_names']

    def clean(self):
        if self.cleaned_data['creater_name'] not in \
            self.cleaned_data['payer_names']+self.cleaned_data['consumer_names']:
            raise forms.ValidationError("You are not involved in the transaction, so don't record it!")
        return self.cleaned_data

class CreateNewRecurringForm(forms.Form):
    creater_name = forms.CharField(required=False,max_length=30)
    subject = forms.CharField(max_length=80)
    message = forms.CharField(required=False,widget=forms.Textarea,max_length=65536)
    amount = forms.FloatField()
    consumer_names = forms.CharField(max_length=65536)
    tags = forms.CharField(max_length=100)
    started_on = forms.DateField()
    period = forms.IntegerField() 
