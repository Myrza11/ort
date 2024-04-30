from django.urls import path
from ort_test.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('passold_ort_test/<int:pk>/', PassTestView.as_view()),
    path('start_ort_test/', StartTestView.as_view()),
    path('get_subject/', SubjectListView.as_view()),
    path('subjects/<int:pk>/tests/', TestListView.as_view()),
    path('topic/<int:pk>/question/', QuestionListView.as_view()),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)