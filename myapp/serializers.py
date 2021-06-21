from rest_framework import serializers
from .models import RecogData, ConversationData, RoomData, Classroom, Lecture

class RecogDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = RecogData
    fields = ['data']

class ConversationDataSerializer(serializers.ModelSerializer):
  user = serializers.ReadOnlyField(source='user.name')
  class Meta:
    model = ConversationData
    fields = ['id','user','data','time']

  def save(self, **kwargs):
    print("saveしたよ")
    # print(kwargs)
    return super().save(**kwargs)

class ClassroomSerializer(serializers.ModelSerializer):
  class Meta:
    model = Classroom
    fields = ['name']

class LectureSerializer(serializers.ModelSerializer):
  class Meta:
    model = Lecture
    fields = ['name', 'room', 'weeK_of_day', 'timed']

class RoomDataSerializer(serializers.ModelSerializer):
  user = serializers.ReadOnlyField(source='user.name')
  # user = UserSerializer()
  class Meta:
    model = RoomData
    fields = ['id','user', 'room', 'enter_at', 'leave_at']

  def validate(self, attrs):
    # print("バリデーション")
    # print(attrs)
    return super().validate(attrs)

  def save(self, **kwargs):
    # print("saveしたよ")
    # print(kwargs)
    return super().save(**kwargs)