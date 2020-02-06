from django.db import models


class Second(models.Model):
	text = models.TextField(max_length=100)
	image = models.CharField(max_length=200)
	answer = models.TextField(max_length=100)
	description = models.TextField(max_length=500, blank=True, null=True)
	option1 = models.CharField(max_length=100)
	ans_true = models.IntegerField(default=0)
	ans_false = models.IntegerField(default=0)
	message_id = models.CharField(max_length=200)
	

	def __str__(self):
		return self.text