from django.db import models


class Channel(models.Model):
	name = models.CharField(max_length=200, blank=True, null=True)
	link = models.CharField(max_length=50, blank=False)

	def __str__(self):
		return self.name

