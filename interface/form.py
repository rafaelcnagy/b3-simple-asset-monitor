
from django import forms
from django.core.exceptions import ValidationError
from .models import AssetMonitoring
from monitoring.models import Asset

class AssetMonitoringForm (forms.ModelForm):
    code = forms.ChoiceField()

    class Meta:
        model = AssetMonitoring
        fields = ['lower_limit', 'upper_limit']

    def __init__(self, *args, **kwargs):
        super(AssetMonitoringForm, self).__init__(*args, **kwargs)
        self.fields['code'].choices = [(asset.id, asset.code) for asset in Asset.objects.all()]
        self.fields['lower_limit'].required = False
        self.fields['upper_limit'].required = False

    def clean(self):
        super(AssetMonitoringForm, self).clean()
        asset = AssetMonitoring.objects.filter(user=self.user, asset=Asset.objects.get(id=self.data['code']))
        if len(asset) > 0:
            raise ValidationError(f'Você já tem esse ativo cadastrado.')

    def save(self):
        asset_monitoring = super(AssetMonitoringForm, self).save(commit=False)
        asset_monitoring.asset = self.asset
        asset_monitoring.user = self.user
        asset_monitoring.save()
