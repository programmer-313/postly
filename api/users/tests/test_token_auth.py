from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class AbstractTokenAuthCase(APITestCase):
    def setUp(self):
        # assign variables for test
        User = get_user_model()
        self.email = "testuser@example.com"
        self.valid_pass = "django-test-client"
        self.invalid_pass = "invalid-client"

        # create test object
        self.user = User(email=self.email)
        self.user.set_password(self.valid_pass)
        self.user.save()


class AbstractRefreshLogoutView(AbstractTokenAuthCase):
    def setUp(self):
        super().setUp()

        # obtain the refresh token for user
        self.ref_token = RefreshToken.for_user(self.user)
        self.inv_ref_tok = "invalid_refresh_token"

        self.valid_data = {"refresh": str(self.ref_token)}
        self.invalid_data = {"refresh": self.inv_ref_tok}
        
        # expected responses for invalid and blacklisted tokens
        self.blacklist_tok_res = {"detail": "Token is blacklisted", "code": "token_not_valid"}
        self.invalid_tok_res = {"detail": "Token is invalid", "code": "token_not_valid"}


class TestTokenLoginView(AbstractTokenAuthCase):
    def setUp(self):
        super().setUp()
        self.valid_creds = {"email": self.email, "password": self.valid_pass}
        self.invalid_creds = {"email": self.email, "password": self.invalid_pass}

        self.url = reverse("obtain_token_login")

    def test_login_valid_creds(self):
        response = self.client.post(self.url, self.valid_creds, format="json")
        data = response.json()
        assert "access" in data
        assert "refresh" in data
        assert "token_version" in data    # checks for new tok. ver. key added
        assert response.status_code == 200

    def test_login_invalid_creds(self):
        response = self.client.post(self.url, self.invalid_creds, format="json")
        out_err = response.json()
        exp_err = {"detail": "No active account found with the given credentials"}

        assert response.status_code == 401
        assert out_err == exp_err


class TestTokenRefreshView(AbstractRefreshLogoutView):
    def setUp(self):
        super().setUp()

        self.url = reverse("refresh_token")

    def test_valid_access_token_generation(self):
        response = self.client.post(self.url, self.valid_data)
        res_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert "access" in res_data
        assert "token_version" in res_data    # checks for new tok. ver. key added

    def test_invalid_refresh_token(self):
        response = self.client.post(self.url, self.invalid_data)
        res_data = response.json()
        exp_data = self.invalid_tok_res

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert res_data == exp_data

    def test_blacklisted_refresh_token(self):
        # blacklist the generated refresh token
        self.ref_token.blacklist()

        # send POST request to client
        response = self.client.post(self.url, self.valid_data)
        res_data = response.json()
        exp_data = self.blacklist_tok_res

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert res_data == exp_data


class TestTokenLogoutView(AbstractRefreshLogoutView):
    def setUp(self):
        super().setUp()

        self.url = reverse("blacklist_token_logout")

    def test_valid_refresh_token_blacklist(self):
        response = self.client.post(self.url, self.valid_data)
        res_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert res_data == {}
    
    def test_invalid_refresh_token_logout(self):
        response = self.client.post(self.url, self.invalid_data)
        res_data = response.json()
        exp_data = self.invalid_tok_res

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert res_data == exp_data

    def test_blacklisted_refresh_token_logout(self):
        # blacklist valid refresh token
        self.ref_token.blacklist()

        # send POST req to url with blacklisted token
        response = self.client.post(self.url, self.valid_data)
        res_data = response.json()
        exp_data = self.blacklist_tok_res

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert res_data == exp_data

 

