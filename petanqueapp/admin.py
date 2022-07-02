from django.contrib import admin
from petanqueapp.models import Player, Match, Round, Tournament

# Register your models here.
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Round)
admin.site.register(Tournament)
