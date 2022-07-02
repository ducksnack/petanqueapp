from django import forms
from petanqueapp.models import Match

class MatchForm(forms.ModelForm):
    class Meta():
        model = Match
        fields = ('player1score', 'player2score', 'player3score')
