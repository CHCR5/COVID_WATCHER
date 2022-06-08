from django.contrib.auth.models import User 
from .models import Empleado 
 
class MyBackEnd(object): 
 
 def authenticate(self, correoaux, password): 

 #check is user is present in User DB. 
  existing_user = User.objects.get(correo=correoaux) 
  if not existing_user: 
   #Checking the user UserData Custom DB. 
   user_data = Empleado.objects.get(correo=correoaux) 
   print("...%s...." % user_data) 
   if correoaux == user_data.correo: 
    user =  User.objects.create_user(username=userid,password=12345) 
    user.save() 
    return user 
   else: 
    return None 
  else: 
   return existing_user 
 
 def get_user(self, user_id): 
 try: 
  return User.objects.get(username=user_id) 
 except User.DoesNotExist: 
  return None 