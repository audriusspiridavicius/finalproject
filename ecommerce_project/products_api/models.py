from django.db import models
from rest_framework.authentication import TokenAuthentication

# Create your models here.
class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"