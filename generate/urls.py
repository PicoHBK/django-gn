from django.urls import path
from .views import (
    ConcatenatePromptsView,
    CharacterListView,
    SkinListByCharacterView,
    SkinListByCharacterAdminView,
    PoseListPreviewView,
    PoseListAllView,
    EmoteListView,
    ImageTypeListView,
    FranchiseListView,
    CharactersByFranchise,
    SpecialListView,
    FranchiseEditById,
    FranchiseDeleteView,
    CharacterEditById,
    SkinEditByEditView,
    FranchiseCreateView,
    CharacterDeleteView,
    CharacterCreateView,
    SkinDeleteView,
    SkinCreateView,
    TagListView,
    SpecialListAdminView,
    SpecialEditByIdView,
    SpecialCreateView,
    SpecialDeleteByIdView,
    TagEditViewById,
    TagDeleteById,
    TagCreateView,
    URLSDEditView,
    PoseListAdminView,
    PoseCreateView,
    PoseDeleteByIdView,
    PoseEditByIdView,
    EmoteListAdminView,
    EmoteCreateView,
    EmoteDeleteByIdView,
    EmoteEditByIdView,
    SpecialPresetListView,
    SpecialPresetCreateView,
    ControlPoseListView
)

urlpatterns = [
    path(
        "concatenate-prompts/",
        ConcatenatePromptsView.as_view(),
        name="concatenate-prompts",
    ),
    path("character/list", CharacterListView.as_view(), name="character-list"),
    path("character/<int:id>/edit", CharacterEditById.as_view(), name="character-edit"),
    path("character/new", CharacterCreateView.as_view(), name="character-new"),
    path("character/<int:id>/delete", CharacterDeleteView.as_view(), name="character-delete"),
    
    
    path("character/<str:name>/skins", SkinListByCharacterView.as_view(), name="skin-list-by-character"),
    path("character/<str:name>/skins/admin", SkinListByCharacterAdminView.as_view(), name="skin-list-by-character-admin"),
    path("character/skin/<int:id>/edit", SkinEditByEditView.as_view(), name="skin-edit-by-character-admin"),
    path("character/skin/<int:id>/delete", SkinDeleteView.as_view(), name="skin-delete-by-character-admin"),
    path("character/skin/new", SkinCreateView.as_view(), name="skin-create-by-admin"),
    path("franchise/<int:id>/characters", CharactersByFranchise.as_view(), name="characters-by-franchise"),
    
    path("pose/preview", PoseListPreviewView.as_view(), name="pose-list"),
    path("pose/all", PoseListAllView.as_view(), name="pose-list-all"),
    path("pose/all/admin",PoseListAdminView.as_view(), name="pose-list-admin"),
    path("pose/new",PoseCreateView.as_view(), name="pose-create-admin"),
    path("pose/<int:id>/edit",PoseEditByIdView.as_view(), name="pose-edit-admin"),
    path("pose/<int:id>/delete",PoseDeleteByIdView.as_view(), name="pose-delete-admin"),
    
    
    
    path("emote/list", EmoteListView.as_view(), name="emote-list"),
    path("emote/<int:id>/edit", EmoteEditByIdView.as_view(), name="emote-list"),
    path("emote/<int:id>/delete", EmoteDeleteByIdView.as_view(), name="emote-list"),
    path("emote/new", EmoteCreateView.as_view(), name="emote-list"),
    path("emote/list/admin", EmoteListAdminView.as_view(), name="emote-list"),
    
    
    
    
    
    path("imagetype/list", ImageTypeListView.as_view(), name="imagetype-list"),
    
    
    path("franchise/new", FranchiseCreateView.as_view(), name="franchises-new"),
    path("franchise/<int:id>/delete", FranchiseDeleteView.as_view(), name="franchises-delete"),
    path("franchise/list", FranchiseListView.as_view(), name="franchises"),
    path("franchise/<int:id>/edit", FranchiseEditById.as_view(), name="franchises-edit"),
    
    
    path("tag/list/admin" ,TagListView.as_view(),name ="tag-list-admin"),
    path("tag/<int:id>/edit" ,TagEditViewById.as_view(),name ="tag-edit-admin"),
    path("tag/<int:id>/delete" ,TagDeleteById.as_view(),name ="tag-delete-admin"),
    path("tag/new" ,TagCreateView.as_view(),name ="tag-create-admin"),
    
    
    path("url/sd",URLSDEditView.as_view(),name ="url-edit"),
    
    
    
    
    path("special/list", SpecialListView.as_view(), name="special-list"),
    path("special/list/admin", SpecialListAdminView.as_view(), name="special-list-admin"),
    path("special/<int:id>/edit", SpecialEditByIdView.as_view(), name="special-edit-admin"),
    path("special/new", SpecialCreateView.as_view(), name="special-create-admin"),
    path("special/<int:id>/delete", SpecialDeleteByIdView.as_view(), name="special-delete-admin"),
    
    
    path("special-preset/list", SpecialPresetListView.as_view(), name="special-preset-list"),
    path("special-preset/new", SpecialPresetCreateView.as_view(), name="special-preset-new"),
    #new
    
    path("controlpose/list", ControlPoseListView.as_view(), name="control-pose-list"),
    
    
]
