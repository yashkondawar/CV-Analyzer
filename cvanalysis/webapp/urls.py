from django.urls import path, include
import webapp.views
urlpatterns = [
    path('',webapp.views.login),
    path('datainp/',webapp.views.datainput),
    path('recommend/',webapp.views.recommend),
    path('finallist/',webapp.views.finallist),
    path('viewcv/',webapp.views.viewcv),
    path('try/',webapp.views.tryal)
]
