
import crypt
import spwd

def authenticate(username,password):
    try:
        user = spwd.getspnam(username)
        print(user)
        if user:
            return crypt.crypt(password, user.sp_pwdp) == user.sp_pwdp , user
    except KeyError:
        return False
    return False

print(authenticate)
