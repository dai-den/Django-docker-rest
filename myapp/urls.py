from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
  path('conversationdata/', views.ConversationDataList.as_view()),
  path('lectures/', views.LectureList.as_view()),
  path('classrooms/', views.ClassRoomList.as_view()),
  path('roomdatas/', views.RoomDataList.as_view()),
  path('roomdatas/<int:pk>/', views.RoomDataDetail.as_view()),
  path('pdfgen/<str:delay>/', views.PdfGenerate.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)