from django.urls import path
from ort_test.views import *


urlpatterns = [
    path('passold_ort_test/', PassOldTestView.as_view()),
    path('start_ort_test/', StartTestView.as_view()),
    path('pass_ort_test/', PassTestView.as_view()),
    path('finish_ort_test/', FinishTestView.as_view()),
    ]