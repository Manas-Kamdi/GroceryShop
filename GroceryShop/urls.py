from django.contrib import admin
from django.urls import path, include, re_path  # ✅ re_path added here
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve  # ✅ serve added here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('GroceryShopApp.urls')),  # your app routes
]

# ✅ Serve media files even in production (like Render)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# ✅ Optionally keep this (helps in local dev)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
