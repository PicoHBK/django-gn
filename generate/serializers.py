from rest_framework import serializers
from .models import Character, Skin, Pose,Emote, ImageType, Franchise,Tag, Special,URLSD



class CharacterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"

class SkinSerializers(serializers.ModelSerializer):
    class Meta:
        model = Skin
        fields = ["id","name","tier","url_img","character"]
class SkinSerializersAdmin(serializers.ModelSerializer):
    class Meta:
        model = Skin
        fields = "__all__"
        
class PoseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pose
        fields = ["name","tier"]
        
class PoseAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pose
        fields = "__all__"

class EmoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Emote
        fields = ["name"]
class EmoteAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = Emote
        fields = "__all__"

class ImageTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageType
        fields = ["name","url_img"]
class FranchiseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']  # Campos básicos para el modelo Tag


###################################333

class SpecialSerializer(serializers.ModelSerializer):  # Solo lectura de tags asociados

    class Meta:
        model = Special
        fields = ["id", "name", "tier"]
class SpecialSerializerAdmin(serializers.ModelSerializer):  # Solo lectura de tags asociados

    class Meta:
        model = Special
        fields = "__all__"
        
######################################3
        
class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        
class URLSDSerializers(serializers.ModelSerializer):
    class Meta:
        model = URLSD
        fields = "__all__"