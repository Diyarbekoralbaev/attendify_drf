from django.urls import path
from .views import EmployeeView, EmployeeDetailView, EmployeeAttendanceView, EmployeeAttendanceDetailView

urlpatterns = [
    path('', EmployeeView.as_view(), name='employees'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('attendance/', EmployeeAttendanceView.as_view(), name='employee_attendance'),
    path('attendance/<int:pk>/', EmployeeAttendanceDetailView.as_view(), name='employee_attendance_detail'),
]
