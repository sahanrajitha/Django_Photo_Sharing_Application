from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.GalleryList.as_view(), name="gallery"),
    path('photo/<str:pk>/', views.PhotoDetail.as_view(), name="photo"),
    path('add/',views.AddPhoto.as_view(), name="add"),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page="login"), name="logout"),
    path('register/', views.RegisterPage.as_view(), name="register"),
    path('add/category', views.AddNewCategory.as_view(), name="category"),
    path('photo/delete/<str:pk>', views.PhotoDelete.as_view(), name="delete"),
    path('photo/update/<str:pk>', views.PhotoUpdate.as_view(), name="update"),
]