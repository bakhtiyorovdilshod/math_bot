from apps.user.models.user import User

def find_rank(user):
	data_list = []
	x = 10
	queryset = User.objects.all().order_by('-numb_of_true_answer')
	for query in queryset:
		data_list.append({
			'user_id':query.user_id
			})
	for i in range(1, len(data_list)+1):
		if data_list[i]['user_id']==str(user):
			return i 
	

	
	









