from django.db import models


class FourChoice(models.Model):
	text = models.TextField(max_length=100)
	image = models.CharField(max_length=200)
	answer = models.TextField(max_length=100)
	option1 = models.CharField(max_length=100)
	option2 = models.CharField(max_length=100)
	option3 = models.CharField(max_length=100)
	description = models.TextField(max_length=500, blank=True, null=True)
	numb_of_option1 = models.IntegerField(default=0, blank=True, null=True)
	numb_of_option2 = models.IntegerField(default=0, blank=True, null=True)
	numb_of_option3 = models.IntegerField(default=0, blank=True, null=True)
	true_answer = models.IntegerField(default=0, blank=True, null=True)
	message_id = models.CharField(max_length=200)
	ans_false = models.IntegerField(default=0, blank=True, null=True)

	def __str__(self):
		return self.text