from django.shortcuts import render
from .serializers import RecogDataSerializer, ConversationDataSerializer, RoomDataSerializer, LectureSerializer, ClassroomSerializer
from .models import RecogData, ConversationData, RoomData, Lecture, Classroom
from rest_framework import generics, permissions
import datetime

import os
from django.conf import settings
from django.http import HttpResponse
from urllib.parse import quote

from rest_framework.views import APIView

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch, mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# Create your views here.

class RecogDataList(generics.ListCreateAPIView):
  queryset = RecogData.objects.all()
  serializer_class = RecogDataSerializer
  # permission_classes = [permissions.IsAdminUser]

class ConversationDataList(generics.ListCreateAPIView):
  queryset = ConversationData.objects.all()
  serializer_class = ConversationDataSerializer
  # permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticated]

  def perform_create(self, serializer):
    print("create")
    serializer.save(user=self.request.user)
  
  def post(self, request, *args, **kwargs):
    print("create2")
    # tmp_time = request.data['time']
    # request.data['time'] = datetime.datetime.fromtimestamp(tmp_time)
    return super().post(request, *args, **kwargs)

class LectureList(generics.ListAPIView):
  queryset = Lecture.objects.all()
  serializer_class = LectureSerializer
  permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticated]

class ClassRoomList(generics.ListAPIView):
  queryset = Classroom.objects.all()
  serializer_class = ClassroomSerializer
  permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticated]

class RoomDataList(generics.ListCreateAPIView):
  queryset = RoomData.objects.all()
  serializer_class = RoomDataSerializer
  permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticated]

  def get_queryset(self):
    duser = self.request.user
    todayData = datetime.date.today()
    return RoomData.objects.filter(user=duser, enter_at__date = todayData)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
  
  def post(self, request, *args, **kwargs):
    tmp_time = request.data['enter_at']
    request.data['enter_at'] = datetime.datetime.fromtimestamp(tmp_time)
    return super().post(request, *args, **kwargs)

class RoomDataDetail(generics.RetrieveUpdateAPIView):
  queryset = RoomData.objects.all()
  serializer_class = RoomDataSerializer
  permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticated]

  def patch(self, request, *args, **kwargs):
    print("viewにて")
    tmp_time = request.data['leave_at']
    request.data['leave_at'] = datetime.datetime.fromtimestamp(tmp_time)
    print(request.data)
    # return Response({"patch":"ok"})
    return super().patch(request, *args, **kwargs)

def zeropadding(time):
  if(time >= 0 and time < 10):
    return '0' + str(time)
  else:
    return str(time)

class PdfGenerate(APIView):
  permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticated]

  def get(self, request, *args, **kwargs):
    print("リクエスト:",self)
    print("リクエスト:",request.data)
    print("リクエスト:",args)
    print("リクエスト:",kwargs)

    # 退館時刻を飛ばしてくる設定で
    # leave_time_from_web = datetime.datetime.now()
    print("退館時刻:",kwargs['delay'])

    roomDatas = RoomData.objects.filter(user=self.request.user, enter_at__date = datetime.date.today())

    filename = 'template.pdf'
    filepath = os.path.join(settings.BASE_DIR, 'myapp/static/template.pdf')
    op = makePdf("user",roomDatas,kwargs['delay'])

    with open(op, 'rb') as pdf:
      response = HttpResponse(content=pdf)
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(filename.encode('utf-8'))}"

    return response

def makePdf(name,roomDatas,leave_time_from_web):
  print(roomDatas)

  now = datetime.date.today()
  template_file = './myapp/static/template.pdf'
  tmp_file = './myapp/__tmp.pdf' # 一時ファイル
  output_file = './myapp/static/output/' + str(now) + 'output.pdf'
  # A4縦のCanvasを作成 -- (*1)
  w, h = portrait(A4)
  cv = canvas.Canvas(tmp_file, pagesize=(w,h))
  # フォントを登録しCanvasに設定 --- (*2)
  font_size = 13
  GEN_SHIN_GOTHIC_MEDIUM_TTF = "./myapp/static/font/GenShinGothic-Monospace-Medium.ttf"
  pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))
  cv.setFont('GenShinGothic', font_size)
  
  # 文字列を描画する --- (*3)
  cv.setFillColorRGB(0, 0, 0)
  cv.drawString(w - 135, h - 91, str(now.month))
  cv.drawString(w - 100, h - 91, str(now.day))

  cv.setFont('GenShinGothic', 15)

  cnt = 0
  for data in roomDatas:
    if(data.room == "入退館"):
      enter_time = data.enter_at.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
      # leave_time = data.leave_at.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
      leave_time = datetime.date.today()

      cv.drawString(78, 483, zeropadding(enter_time.hour))
      cv.drawString(105, 483, zeropadding(enter_time.minute))
      cv.drawString(132, 483, leave_time_from_web[0:2])
      cv.drawString(156, 483, leave_time_from_web[3:5])
      continue
    
    enter_time = data.enter_at.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
    leave_time = data.leave_at.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

    print(type(int(enter_time.hour)))
    print(enter_time.hour)
    cv.drawString(187, 458 - cnt * 25.8, data.room)
    cv.drawString(273, 458 - cnt * 25.8, zeropadding(int(enter_time.hour)))
    cv.drawString(299, 458 - cnt * 25.8, zeropadding(int(enter_time.minute)))
    cv.drawString(322, 458 - cnt * 25.8, zeropadding(int(leave_time.hour)))
    cv.drawString(346, 458 - cnt * 25.8, zeropadding(int(leave_time.minute)))
    cnt = cnt + 1
    
  # cv.drawString(70*mm, h-150*mm, "クジラ飛行机")
  # 一時ファイルに保存 --- (*4)
  cv.showPage()
  cv.save()
  # テンプレートとなるPDFを読む --- (*5)
  template_pdf = PdfFileReader(template_file)
  template_page = template_pdf.getPage(0)
  # 一時ファイルを読んで合成する --- (*6)
  tmp_pdf = PdfFileReader(tmp_file)
  template_page.mergePage(tmp_pdf.getPage(0))
  # 書き込み先PDFを用意 --- (*7)
  output = PdfFileWriter()
  output.addPage(template_page)
  with open(output_file, "wb") as fp:
    output.write(fp)
  return output_file