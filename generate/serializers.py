from rest_framework import serializers
from .models import Character, Skin, Pose,Emote, ImageType



class CharacterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"

class SkinSerializers(serializers.ModelSerializer):
    class Meta:
        model = Skin
        fields = ["id","name","tier","url_img"]
        
class PoseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pose
        fields = ["name","tier"]

class EmoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Emote
        fields = ["name"]

class ImageTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageType
        fields = ["name","url_img"]
        