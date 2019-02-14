from django.db import models

class Host(models.Model):
    name = models.CharField(max_length=100) # unique=True
    #year_of_release = models.PositiveSmallIntegerField()
    # "required" is a valid argument for Django forms. For models, blank=True (for the admin) and null=True (for the database).
    pub_date = models.DateField('date published', blank=True, null=True)
    ipv4 = models.GenericIPAddressField()
    # use related_name since we don't want to use host_set (RelatedManager)
    bound_for = models.ForeignKey('self', models.SET_NULL, blank=True, null=True, related_name='bebound')
    # to know who created this host
    creater = models.ForeignKey('auth.User', models.SET_NULL, blank=True, null=True, related_name='host')

    def __str__(self):
        return self.name
