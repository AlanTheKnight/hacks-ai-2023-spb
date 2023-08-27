from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("backend.authentication.urls")),
    path("api/", include("backend.api.urls")),
    path("", never_cache(TemplateView.as_view(template_name="index.html")), name="index")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static("/_nuxt/", document_root=settings.BASE_DIR / "output" / "_nuxt")
urlpatterns += static("/", document_root=settings.BASE_DIR / "output")
