from django.test import TestCase
#python manage.py test

class SimpleTest(TestCase):
    def test_should_be_equal(self):
        self.assertEqual(1,1)