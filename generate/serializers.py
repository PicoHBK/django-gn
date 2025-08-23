from rest_framework import serializers
from .models import Character, ControlPose, Skin, Pose,Emote, ImageType, Franchise,Tag, Special,URLSD,SpecialPreset



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
    special_disabled = serializers.SerializerMethodField()
    
    class Meta:
        model = Pose
        fields = ["name","tier","img_type","special_disabled"]
    
    def get_special_disabled(self, obj):
        return [special.name for special in obj.special_disabled.all()]
        
class PoseAdminSerializers(serializers.ModelSerializer):
    special_disabled = serializers.SerializerMethodField()
    
    class Meta:
        model = Pose
        fields = "__all__"
    
    def get_special_disabled(self, obj):
        return [special.name for special in obj.special_disabled.all()]

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
        fields = ["name","url_img","id"]
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
        
class SpecialPresetSerializers(serializers.ModelSerializer):
    class Meta:
        model = SpecialPreset
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

class ControlPoseSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = ControlPose
        fields = "__all__"