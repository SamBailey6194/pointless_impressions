from django.urls import path
from . import views


# URL patterns for the search app
app_name = 'search'

urlpatterns = [
    path(
        '',
        views.SearchView.as_view(),
        name='search_results'
        ),
    path(
        'api/autocomplete/',
        views.SearchAutocompleteView.as_view(),
        name='search_autocomplete'
        ),
]
