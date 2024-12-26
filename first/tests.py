from django.test import TestCase, Client
from django.urls import reverse

class IndexText(TestCase):

    def test_index_response(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

# Create your tests here.
