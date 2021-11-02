from django.db import models


class GameType(models.Model):

    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label