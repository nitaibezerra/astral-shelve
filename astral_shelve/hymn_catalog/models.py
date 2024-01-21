from django.db import models

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_information = models.CharField(max_length=255)

class Hymn(models.Model):
    STYLE_CHOICES = [
        ('marcha', 'Marcha'),
        ('valsa', 'Valsa'),
        ('mazurca', 'Mazurca'),
    ]

    hymn_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    number = models.IntegerField()
    hymn_order = models.IntegerField()
    title = models.CharField(max_length=255)
    lyrics = models.TextField(blank=True, null=True)
    date_received = models.DateField()
    offered_to_person = models.ForeignKey(Person, related_name='offered_hymns', on_delete=models.SET_NULL, null=True, blank=True)
    style = models.CharField(max_length=10, choices=STYLE_CHOICES)
    repetitions = models.CharField(max_length=255, blank=True, null=True)
    footnote = models.TextField(blank=True, null=True)

class Strophe(models.Model):
    strophe_id = models.AutoField(primary_key=True)
    hymn = models.ForeignKey(Hymn, on_delete=models.CASCADE)
    strophe_order = models.IntegerField()
    text = models.TextField()
