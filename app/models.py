from django.db import models

class Contact(models.Model):
    course_string = models.CharField(max_length=20)
    # session = models.CharField(max_length=1, choices=[('W', 'Winter'), ('S', 'Summer')])
    # year = models.CharField(max_length=4)
    # dept = models.CharField(max_length=4)
    # course = models.CharField(max_length=4)
    # section = models.CharField(max_length=3)
    only_general = models.BooleanField()
    sms = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=30)

    class Meta:
        unique_together = (('course_string', 'email'))

    def __str__(self):
        return " ".join[self.course_string, str(self.only_general), self.sms, self.email]