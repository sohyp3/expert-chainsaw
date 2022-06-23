from django import forms 
from .models import linksModel, jsUseragentModel

class linkForm(forms.ModelForm):
    class Meta:
        model = linksModel
        fields = ['windowsURL','macURL','androidURL','iosURL','otherURL','notes']


class jsUseragentForm(forms.ModelForm):
    class Meta:
        model = jsUseragentModel
        fields = ['browser_codeName','browser_version','browser_language','cookies_enabled','platform',"user_agent_header","timezone_utc","timezone_place","screen_size","battery_level",]
