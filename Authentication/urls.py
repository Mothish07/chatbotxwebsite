from django.urls import path
from Authentication import views as authViews
from MainPage import views as mainViews
urlpatterns = [
   path('',authViews.home,name = 'home'),
   path('signup/',authViews.signup,name = 'signup'),
   path('signin',authViews.signin,name='signin'),
   path('signout',authViews.signout,name='signout'),
   path('resetPassword',authViews.resetPassword,name='resetPassword'),
   path('generate_reply/', mainViews.generate_reply, name='generate_reply'),
   path('convert_voice_to_text/',mainViews.convert_voice_to_text,name ='convert_voice_to_text' ),
   path('get_chat_history/', mainViews.get_chat_history, name='get_chat_history'),
   path('save_chat/', mainViews.save_chat, name='save_chat'),
   path('delete_chat_history/', mainViews.delete_chat_history, name='delete_chat_history'),

]
