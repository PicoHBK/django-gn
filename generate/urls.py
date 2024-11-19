from django.urls import path
from .views import (
    ConcatenatePromptsView,
    CharacterListView,
    SkinListByCharacterView,
    PoseListView,
    EmoteListView,
    ImageTypeListView,
)

urlpatterns = [
    path(
        "concatenate-prompts/",
        ConcatenatePromptsView.as_view(),
        name="concatenate-prompts",
    ),
    path("character/list", CharacterListView.as_view(), name="character-list"),
    path("character/<str:name>/skins", SkinListByCharacterView.as_view(), name="skin-list-by-character"),
    path("pose/list", PoseListView.as_view(), name="pose-list"),
    path("emote/list", EmoteListView.as_view(), name="emote-list"),
    path("imagetype/list", ImageTypeListView.as_view(), name="imagetype-list"),
    
]
