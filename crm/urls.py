from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.permissions import AllowAny
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from users.api.views import RegistrationView, LoginView

schema_view = get_schema_view(
    openapi.Info(
        title="api",
        default_version='v1',
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path(f"login-social/<str:backend>{extra}", authtest, name="begin"),
    # path(f"test/<str:backend>", TestView.as_view(), name="test"),
    # path(f"login/complete/<str:backend>{extra}", complete, name="complete"),
    # path(f"login/complete/<str:backend>{extra}", CompleteView.as_view(), name="complete"),
    # re_path(r'^social/jwt-pair/(?:(?P<provider>[a-zA-Z0-9_-]+)/?)?$',
    #         SocialJWTPairOnlyAuthView.as_view(),
    #         name='login_social_jwt_pair'),
    path('api/', include([
       path('', include('bookmarks_manager.api.urls')),
    ])),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
