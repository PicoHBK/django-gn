from django.urls import path
from .views import (
    ConcatenatePromptsView,
    CharacterListView,
    SkinListByCharacterView,
    PoseListPreviewView,
    PoseListAllView,
    EmoteListView,
    ImageTypeListView,
    FranchiseListView,
    CharactersByFranchise,
    SpecialListView
)

urlpatterns = [
    path(
        "concatenate-prompts/",
        ConcatenatePromptsView.as_view(),
        name="concatenate-prompts",
    ),
    path("character/list", CharacterListView.as_view(), name="character-list"),
    path("character/<str:name>/skins", SkinListByCharacterView.as_view(), name="skin-list-by-character"),
    path("pose/preview", PoseListPreviewView.as_view(), name="pose-list"),
    path("pose/all", PoseListAllView.as_view(), name="pose-list-all"),
    path("emote/list", EmoteListView.as_view(), name="emote-list"),
    path("imagetype/list", ImageTypeListView.as_view(), name="imagetype-list"),
    path("franchise/list", FranchiseListView.as_view(), name="franchises"),
    path("franchise/<int:id>/characters", CharactersByFranchise.as_view(), name="characters-by-franchise"),
    path("special/list", SpecialListView.as_view(), name="special-list"),
    
]
