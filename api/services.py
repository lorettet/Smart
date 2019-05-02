from api.models import User

def login(email, password):
    try:
        return User.objects.get(email=email,password=password)
    except User.DoesNotExist:
        return None


def createUser(firstname,lastname,email,password):
    u = User(firstname,lastname,email,password)
    u.save()
