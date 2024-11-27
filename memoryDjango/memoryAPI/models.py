from django.db import models

class Person(models.Model):
    id = models.IntegerField(primary_key=True)  # Explicitly define ID as IntegerField
    name = models.CharField(max_length=255)
    birth = models.IntegerField()

    def __str__(self):
        return self.name

class Event(models.Model):
    id = models.IntegerField(primary_key=True)  # Explicitly define ID as IntegerField
    event = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return self.event

class Participation(models.Model):
    person = models.ForeignKey(
        Person,  # Refer to the model class
        on_delete=models.CASCADE,
        to_field="id",  # Explicitly specify the `id` field
        db_column="person_id",  # Map to an `id` column in the database
        related_name="participations"
    )
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        to_field="id",  # Explicitly specify the `id` field
        db_column="event_id",  # Map to an `id` column in the database
        related_name="participants"
    )

    def __str__(self):
        return f"{self.person.name} participated in {self.event.event}"
