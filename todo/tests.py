from django.test import TestCase
from .models import Task
from datetime import date, timedelta

# Create your tests here.
class TestCalc(TestCase):

    def test_create_task(self):
        task = create_task('foo')
        self.assertEqual(task.title, 'foo')
        self.assertEqual(task.date, date.today())
        self.assertIsNone(task.user)
        self.assertIsNone(task.description)

    def test_get_task(self):
        task = create_task('foo')
        task.save()
        self.assertEqual(task, get_task('foo'))

    def test_not_today(self):
        tomorrow = date.today() + timedelta(days=1)
        task = Task.objects.create(title='foo', date=date.today())
        new_date = not_today(task)
        self.assertEqual(tomorrow, new_date)

def create_task(title):
    task = Task.objects.create(title=title, date=date.today())
    return task

def get_task(title):
    task = Task.objects.get(title=title)
    return task

def not_today(task):
    task.date = task.date + timedelta(days=1)
    return task.date