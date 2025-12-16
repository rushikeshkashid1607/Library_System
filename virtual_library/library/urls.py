from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('', views.book_list, name='book_list'),
    path('category/<str:category>/', views.book_list_by_category, name='book_list_by_category'),

    # path('category/<str:category_name>/<int:book_id>/', views.book_detail, name='book_detail_with_category'),

    # # path('category/<str:category_name>/<int:book_id>/', views.book_detail, name='book_detail_with_category'),
    # path('category/<str:category>/<int:pk>/', views.book_detail, name='book_detail_with_category'),

    # For category with name
    path('category/<str:category_name>/<int:pk>/', views.book_detail, name='book_detail_with_category'),

    # For category with category
    path('category/<str:category>/<int:pk>/', views.book_detail, name='book_detail_with_category'),


    path('<int:pk>/', views.book_detail, name='book_detail'),
    # path('', views.home, name='book_list'), # Add this line for the root path
    path('chatbot/', views.chatbot, name='chatbot'),

    path('aboutus/', views.about_us, name='about_us'),  # New URL path
]
