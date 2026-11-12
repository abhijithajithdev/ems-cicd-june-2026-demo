#default router is a class that automatically creates url for viewset
from rest_framework.routers import DefaultRouter, path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

router=DefaultRouter()
router.register(r'employees',views.employeeViewSet)
router.register(r'departments',views.departmentViewSet)
router.register(r'projects',views.ProjectViewset)
router.register

#signup apiview is an api view not the view set
urlpatterns=[
    path("signup/",views.SignupAPIView.as_view(),name="user_signup"),
    path("login/",views.LoginAPIView.as_view(),name="userlogin"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
]

urlpatterns+=router.urls