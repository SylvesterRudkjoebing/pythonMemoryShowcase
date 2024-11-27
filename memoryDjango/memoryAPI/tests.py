from django.test import TestCase
from django.urls import reverse
from memoryAPI.models import Person, Event, Participation

class ModelTests(TestCase):

    def test_create_person(self):
        person = Person(name='Alice', birth=1990)
        self.assertEqual(person.name, 'Alice')
        self.assertEqual(person.birth, 1990)

    def test_create_event(self):
        event = Event(event='Python Conference', year=2023)
        self.assertEqual(event.event, 'Python Conference')
        self.assertEqual(event.year, 2023)

    def test_create_participation(self):
        person = Person(name='Alice', birth=1990)
        event = Event(event='Python Conference', year=2023)
        participation = Participation(person=person, event=event)

        self.assertEqual(participation.person.name, 'Alice')
        self.assertEqual(participation.event.event, 'Python Conference')

class ViewTests(TestCase):

    def test_index_redirect(self):
        # Test the root URL redirects to the memoryAPI/index page
        response = self.client.get('/')
        self.assertRedirects(response, reverse('memoryAPI:index'))

    def test_index_page(self):
        # Test that the /memoryAPI/index page returns a 200 status code
        response = self.client.get(reverse('memoryAPI:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All Rows in Table")  # Check if the page contains a title or text

    def test_all_rows_in_table(self):
        # Create test data
        person = Person(id = 1337, name='Alice', birth=1990)
        person.save()
        event = Event(id = 2674, event='Python Conference', year=2023)
        event.save()

        # Test the page rendering with actual data in the table
        response = self.client.get(reverse('memoryAPI:index'))
        self.assertContains(response, 'Alice')  # Check if the table contains the person's name
        self.assertContains(response, 'Python Conference')  # Check if the table contains the event name

class PersonFormTests(TestCase):
    def test_create_person_form(self):
        # Initial count of Person objects
        rows = Person.objects.count()

        # Print the count before the form submission
        print("Before form submission:", Person.objects.count())

        # Test the form submission to add a person, omit 'id' field
        response = self.client.post(reverse('memoryAPI:index'), {
            'name': 'Bob',
            'birth': 1985
        })

        # Check that the new person was added to the database
        self.assertEqual(Person.objects.count(), rows + 1)

        # Fetch the person created
        person = Person.objects.last()  # Get the last created person
        self.assertEqual(person.name, 'Bob')
        self.assertEqual(person.birth, 1985)

        # Ensure the form redirects to the index page after submission
        self.assertRedirects(response, reverse('memoryAPI:index'))