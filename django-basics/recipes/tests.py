from django.test import TestCase
#python manage.py test

class SimpleTest(TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)
