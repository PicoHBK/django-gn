from django.contrib import admin
from .models import ControlPose, Franchise, Character, Pose, Skin, Emote, ImageType, URLSD, Tag, Special, SpecialPreset
from django.utils.html import format_html

# Registro de la franquicia en el admin
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Franchise, FranchiseAdmin)

# Registro del personaje en el admin
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'franchise')
    search_fields = ('name', 'franchise__name')  # Busca tanto por nombre de personaje como por franquicia
    list_filter = ('franchise',)
    ordering = ('name',)

admin.site.register(Character, CharacterAdmin)

# Registro de las poses en el admin
class PoseAdmin(admin.ModelAdmin):
    list_display = ('name', 'prompt')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Pose, PoseAdmin)

# Registro de las skins en el admin
class SkinAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'prompt')
    search_fields = ('name', 'character__name')
    list_filter = ('character',)
    ordering = ('name',)

admin.site.register(Skin, SkinAdmin)

# Registro de los emotes en el admin
class EmoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'prompt')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Emote, EmoteAdmin)

# Registro de los tipos de imagen en el admin
class ImageTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'prompt')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(ImageType, ImageTypeAdmin)
admin.site.register(URLSD)
admin.site.register(Tag)
admin.site.register(Special)
admin.site.register(SpecialPreset)

class ControlPoseAdmin(admin.ModelAdmin):
    list_display = ("image_preview",)  # Solo muestra la imagen en la lista
    readonly_fields = ("image_preview",)  # Hace que la imagen aparezca en la edición pero no sea editable

    def image_preview(self, obj):
        if obj.url_img:
            return format_html(
                '<img src="{}" style="max-height:60px; max-width:60px;"/>', obj.url_img
            )
        return "No image"

    image_preview.short_description = "Preview"  # Nombre en el admin

admin.site.register(ControlPose, ControlPoseAdmin)

