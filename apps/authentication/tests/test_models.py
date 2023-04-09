from django.test import TestCase
from django.contrib.auth.models import User
from apps.trips.models import Country
from apps.authentication.models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.profile = Profile.objects.create(user=self.user, image='somebase64', nationality=self.country)

    # Test that data stored data is the same as the data passed when creating
    def test_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.nationality, self.country)
        self.assertEqual(self.profile.image, 'somebase64')

    # Ensure that string representatinon of profile object is correct
    def test_string(self):
        self.assertEqual(str(self.profile), 'someusername')
        
    
