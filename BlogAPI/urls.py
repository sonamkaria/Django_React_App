from django.urls import path, include
from .views import Blog, BlogDetail

urlpatterns = [
    #/people GET / POST these are the only paths this will hit
    path('', Blog.as_view(), name='Blog'),
    path('<slug:slug>', BlogDetail.as_view(), name='BlogDetail')
  
    
]