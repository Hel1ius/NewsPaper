from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignUpForm(SignupForm):
    def save(self, request):
        user = super(BasicSignUpForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user