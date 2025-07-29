from django.urls import path
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    TaskList, TaskDetail, TaskCreate, TaskUpdate,
    DeleteView, CustomLoginView, RegisterPage, TaskReorder,
    TaskFileDelete  # ✅ Correct class-based view import
)

urlpatterns = [
    # 🔐 Auth routes
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    # 🔁 Password reset flow
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # ✅ Core Task app routes
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),

    # 🗑️ Media file delete route
    path('delete-file/<int:pk>/', TaskFileDelete.as_view(), name='delete-file'),  # ✅ Fixed
]

# 📁 Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
