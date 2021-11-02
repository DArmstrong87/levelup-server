from django.contrib import admin
from levelupapi.models import Game, Event, GameType, Gamer, EventGamer
# Register your models here.
admin.site.register(Game)
admin.site.register(Event)
admin.site.register(GameType)
admin.site.register(Gamer)
admin.site.register(EventGamer)
