from django.views.generic import TemplateView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Prefetch
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkCategory, ArtworkFramingCondition
    )
from pointless_impressions_src.photo.models import Photo
# from pointless_impressions_src.blog.models import BlogPost
from pointless_impressions_src.profiles.models import Artist


# Create your views here.
# ---------------------------
# Helper Functions
# ---------------------------
def get_placeholder_image():
    """Returns a placeholder image data."""
    try:
        return Photo.objects.get(asset_identifier='noimage_placeholder')
    except Photo.DoesNotExist:
        return None


# ---------------------------
# Search Results View
# ---------------------------
class SearchView(TemplateView):
    """
    Renders the global search results page, compiling results from multiple
    models (currently Artwork and related fields).

    This view retrieves relevant objects based on the user's query and applies
    pagination.

    **Context**
    - ``results``: A paginated list of objects matching the search query.
    - ``page_obj``: Pagination object for navigating pages.
    - ``search_query``: The original search term entered by the user.

    **URL Parameters**
    - ``q``: The primary query parameter (e.g., /search/?q=sunset).

    **Template:**
    :template:`search/search_list.html`
    """
    template_name = 'search/search_list.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')

        combined_list = []

        if query:
            # Get artwork results
            artwork_search_q = (
                Q(name__icontains=query) |
                Q(artist__user__username__icontains=query) |
                Q(artist__user__first_name__icontains=query) |
                Q(artist__user__last_name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(selected_conditions__condition_name__icontains=query)
            )
            artwork_results = Artwork.objects.filter(
                is_available=True
            ).filter(artwork_search_q).distinct().select_related(
                'category',
                'main_photo',
                'artist',
                'artist__user'
            ).prefetch_related(
                'photos',
                Prefetch(
                    'selected_conditions',
                    queryset=ArtworkFramingCondition.objects.all()
                )
            )

            # Get Blog results
            # blog_search_q = (
            #     Q(title__icontains=query) |
            #     Q(content__icontains=query) |
            #     Q(author__username__icontains=query) |
            #     Q(categories__name__icontains=query) |
            #     Q(excerpt__icontains=query)
            # )
            # blog_results = BlogPost.objects.filter(
            #     is_published=True
            # ).filter(blog_search_q).distinct().select_related(
            #     'author', 'featured_image'
            # )

            # Get Artist results
            artist_search_q = (
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__username__icontains=query) |
                Q(bio__icontains=query)
            )
            artist_results = Artist.objects.filter(
                user__is_active=True
            ).filter(artist_search_q).distinct().select_related(
                'user',
                'user__userprofile__profile_picture'
            )

            # Combine all results
            combined_list = [
                {'model_name': 'artwork', 'object': item}
                for item in artwork_results
            ] + [
                # {'model_name': 'blogpost', 'object': item}
                # for item in blog_results]
            ] + [
                {'model_name': 'artist', 'object': item}
                for item in artist_results
            ]

            paginator = Paginator(combined_list, self.paginate_by)
            page_number = self.request.GET.get('page')

            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)

        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['results'] = page_obj
        context['search_query'] = query
        context['is_paginated'] = context['paginator'].num_pages >= 1
        context['production'] = not settings.DEBUG
        context['placeholder_image'] = get_placeholder_image()
        return context


# ---------------------------
# Search Autocomplete View
# ---------------------------
class SearchAutocompleteView(View):
    """
    Provides JSON responses for search autocomplete functionality.

    This view processes AJAX requests containing a search term and returns
    a list of matching Artwork names to assist users in quickly finding items.

    **URL Parameters**
    - ``term``: The search term input by the user
        (e.g., /search/autocomplete/?term=sun).

    **Response Format**
    - JSON array of strings representing matching Artwork names.

    **Example Response**
    .. code-block:: json

        [
            "Sunset Overdrive",
            "Sunny Meadows",
            "Sunrise Bliss"
        ]
    """
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')

        if len(term) < 2:
            return JsonResponse([], safe=False)

        artwork_matches = Artwork.objects.filter(
            is_available=True,
            name__icontains=term
        ).values_list('name', flat=True)

        category_matches = ArtworkCategory.objects.filter(
            name__icontains=term
        ).values_list('name', flat=True)

        condition_matches = ArtworkFramingCondition.objects.filter(
            condition_name__icontains=term
        ).values_list('condition_name', flat=True)

        artist_matches = Artist.objects.filter(
            user__is_active=True,
            user__username__icontains=term
        ).values_list('name', flat=True)

        combined_results = set(artwork_matches)
        combined_results.update(category_matches)
        combined_results.update(condition_matches)
        combined_results.update(artist_matches)

        final_list = sorted(list(combined_results))[:10]

        return JsonResponse(final_list, safe=False)
