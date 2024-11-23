from django.urls import path
from .views import ClientView, ClientDetailView, ClientVisitHistoryView, ClientVisitHistoryDetailView

urlpatterns = [
    path('', ClientView.as_view(), name='clients'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('visit-history/', ClientVisitHistoryView.as_view(), name='visit_history'),
    path('visit-history/<int:pk>/', ClientVisitHistoryDetailView.as_view(), name='visit_history_detail'),
]