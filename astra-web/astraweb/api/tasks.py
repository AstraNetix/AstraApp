from celery import task

class UserReminders:
	@task
	def remind_email(self, user):
		user.remind_validate_email()