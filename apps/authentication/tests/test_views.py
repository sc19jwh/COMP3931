from django.test import TestCase, Client
from django.urls import resolve, reverse
from apps.authentication.views import *
from django.contrib.auth.models import User
from apps.trips.models import Country

# Verify correct authorisation and redirection for urls
class ViewAuthRedirectTest(TestCase):
    def setUp(self):
        # Set up client
        self.client = Client()
        # Create first user account
        self.username = 'someusername'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.profile = Profile.objects.create(user=self.user, nationality=self.country)

    # Make sure a guest can access user/signin
    def test_signin_guest(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    # Make sure a guest can access user/register
    def test_register_guest(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    # Make sure a guest can't access profile
    def test_profile_guest(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    # Make sure a guest can't access setcountry
    def test_setcountry_guest(self):
        response = self.client.get(reverse('setcountry'))
        self.assertEqual(response.status_code, 302)

    # Log user in and make sure they can't access user/signin
    def test_signin_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 302)

    # Log user in and make sure they can't access user/register
    def test_register_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)

    # Log user in and make sure they can't access user/signin
    def test_profile_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    # Log user in and make sure they can't access user/register
    def test_setcountry_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('setcountry'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'setcountry.html')

# Verify the functionality of all authentication functionality
class AuthenticationFunctionalityTests(TestCase):
    def setUp(self):
        # Set up client
        self.client = Client()
        # Create first user account and login
        self.username = 'someusername'
        self.email = 'someusername@email.com'
        self.password = 'Somepassword20'
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)
        self.country = Country.objects.create(name = "Great Britain", alpha2code = "GB", currency = "GBP", is_interrail = True)
        self.profile = Profile.objects.create(user=self.user)

    # Test signin by signing in with correct details and ensuring a redirect to trip dashboard (which you can't access without being signed in)
    def test_signin_valid(self):
        # Need to ensure that the user profile has a nationality
        Profile.objects.filter(user=self.user).update(nationality=self.country)
        response = self.client.post(reverse('signin'), {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('mytrips', args=[self.user.username]))

    # Test signin by providing incorrect credientials by ensuring that the response reflects that
    def test_signin_invalid(self):
        response = self.client.post(reverse('signin'), {'username': 'someusername', 'password': 'differentpass'})
        self.assertContains(response, 'Your username or password is incorrect.')

    # Test signout by logging in, using the view to signout and checking it redirected back to the landing page (which you can't access if signed in)
    def test_signout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, reverse('main'))

    # Enter completely valid register inputs and ensure that the user is saved and are redirected to the next stage
    def test_register_valid(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'name',
            'last_name': 'name',
            'username': 'username1',
            'email': 'name@mail.com',
            'password1': 'PasS12345'
        })
        self.assertRedirects(response, reverse('setcountry'))
        self.assertTrue(User.objects.filter(username='username1').exists())

    # Enter invalid register inputs and ensure that the appropriate errors are shown and that the account was not created
    def test_register_invalid_inputs(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'name',
            'last_name': 'name',
            'username': 'username1',
            'email': 'email',
            'password1': 'pass'
        })
        self.assertContains(response, "Enter a valid email address.")
        self.assertContains(response, "Password must be at least 8 characters long and be a combination of uppercase, lowercase and numbers.")
        self.assertFalse(User.objects.filter(username='username1').exists())

    # Enter invalid register inputs and ensure that the appropriate errors are shown and that the account was not created
    def test_register_invalid_user_exists(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'name',
            'last_name': 'name',
            'username': 'someusername',
            'email': 'someusername@email.com',
            'password1': 'Somepassword20'
        })
        self.assertContains(response, "A user with that username already exists")
        self.assertContains(response, "A user with that email already exists")
        self.assertTrue(len(User.objects.filter(username='someusername')) == 1)

    # Save nationality against user profile and check redirects correctly and that save has been made to DB
    def test_setcountry_save_nationality(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('setcountry'), {'country': self.country.id})
        self.assertRedirects(response, reverse('mytrips', args=[self.user.username]))
        self.assertEqual(Profile.objects.get(user=self.user).nationality, self.country)

    # Testing get flag by passing a valid country and ensuring the page is displayed correctly 
    def test_set_country_flag_with_id(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('set_country_flag'), {'country': self.country.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/set_country_flag.html')

    # Testing get flag by passing no country and ensuring a bad response error is returned
    def test_set_country_flag_with_no_id(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('set_country_flag'), {})
        self.assertEqual(response.status_code, 400)