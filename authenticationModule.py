import pyrebase
import firebase_admin
from firebase_admin import credentials, auth


cred = credentials.Certificate("/home/mothish/Projects/ChatBotXWeb/credintials/firebaseCredintials.json")
firebase_admin.initialize_app(cred)

firebaseConfig = {
   "apiKey": "AIzaSyCOLYfF47_xfkTEZy8X3A4hwUFaCyLCals",
   "authDomain": "chatbotx-338c8.firebaseapp.com",
   "projectId": "chatbotx-338c8",
   "storageBucket": "chatbotx-338c8.appspot.com",
   "messagingSenderId": "346958153567",
   "databaseURL":"https://trialauth-7eea1.firebaseio.com",
   "appId": "1:346958153567:web:a52241681709cf73e8d8ea",
   "measurementId": "G-YKGQFC8GNV"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth_pyrebase = firebase.auth()

def signUp(name,email,password,cpassword):
   try:
      if len(password) < 8:
         return {"success":False ,"response_msg":"Password is weak... Please Give more than 8 characters!"}
      elif password != cpassword:
         return {"success":False ,"response_msg":"Mismatched the Reconfirmation Password Please Check !"}
      else:
         new_user = auth_pyrebase.create_user_with_email_and_password(email,password)
         uid = new_user["localId"]
         user = auth.update_user(uid,display_name=name)
         auth_pyrebase.send_email_verification(new_user["idToken"])
         return {"success":True ,"user":name,"response_msg":"Successfully Signed Up",'uid':uid}   
   except Exception as e:
      error_message = str(e)
      if "INVALID_EMAIL" in error_message:
         return {"success": False, "response_msg": "Invalid email format. Please enter a valid email address."}
      elif "EMAIL_EXISTS" in error_message:
            return {"success": False, "response_msg": "Email already registered. Please use a different email address."}
      else:
         return {"success": False, "response_msg":f"Something Went Wrong Please Try again!!{e}"}
  


def signIn(email,password):
   try:
      user = auth_pyrebase.sign_in_with_email_and_password(email,password)

      return {"success":True ,"user":user["displayName"],"response_msg":"Sucessfully Signed In" ,'uid':user["localId"]}
   except Exception as e:
        if "INVALID_LOGIN_CREDENTIALS" in str(e):
            return {"success": False, "response_msg": "Invalid login credentials.."}
        elif "INVALID_EMAIL" in str(e):
           return {"success": False, "response_msg": "Invalid Email ID.."}
        else:
           return {"success":False,"response_msg":"Something Went Wrong Please Try again!!!"}
   
      
   
def signOut():
   try:
      auth_pyrebase.current_user = None
      return {"success": True, "response_msg": "Successfully signed out."}

   except Exception:
      return {"success":False,"response_msg":"Something Went Wrong Please Try again!!!"}
   
def reset_password(email):
    try:
        auth_pyrebase.send_password_reset_email(email)
        return {"success": True,"response_msg": "Check Your Registered Email!"}
    except Exception as e:
        if "EMAIL_NOT_FOUND" in str(e):
            return {"success": False, "response_msg": "No User Found in this email. Please Check Email or Create New Account"}
        elif "INVALID_EMAIL" in str(e):
           return {"success": False, "response_msg": "Invalid Email ID.."}
        else:
            return {"success":False,"response_msg":"Something Went Wrong Please Try again!!!"}
def google_signin():
    try:
        # Use Firebase Google Sign-In
        provider = firebase.auth.GoogleAuthProvider()
        user = firebase.auth.signInWithPopup(provider)
        # Access user information
        username = user["displayName"]
        
        return {"success": True, "user": username, "response_msg": "Successfully signed in with Google"}

    except Exception as e:
        return {"success": False, "response_msg": f"Google Sign-In error: {str(e)}"}


def google_signout():
    try:
        auth_pyrebase.current_user = None
        return {"success": True, "response_msg": "Successfully signed out with Google"}

    except Exception as e:
        return {"success": False, "response_msg": f"Google Sign-Out error: {str(e)}"}
   
#test
'''
response = signUp('MothishTest','mothish726@gmail.com','123456789','123456789')
if response['success']:
   print("Successfull")
else:
   print("Failed")
        
'''
