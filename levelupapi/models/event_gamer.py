from django.db import models

class EventGamer(models.Model):

    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.gamer.user.first_name} attending {self.event.game.title} on {self.event.date}"
    