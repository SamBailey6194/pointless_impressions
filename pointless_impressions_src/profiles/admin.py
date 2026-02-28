from django.contrib import admin
from .models import (
    UserProfile, Customer, Artist, StaffRole, Address
)


class CustomerInline(admin.StackedInline):
    model = Customer
    extra = 0


class ArtistInline(admin.StackedInline):
    model = Artist
    extra = 0


class StaffRoleInline(admin.StackedInline):
    model = StaffRole
    extra = 0


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


class IsCustomerFilter(admin.SimpleListFilter):
    title = 'Customer'
    parameter_name = 'is_customer'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(customers__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(customers__isnull=True)
        return queryset


class IsArtistFilter(admin.SimpleListFilter):
    title = 'Artist'
    parameter_name = 'is_artist'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(artists__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(artists__isnull=True)
        return queryset


class IsStaffFilter(admin.SimpleListFilter):
    title = 'Staff'
    parameter_name = 'is_staff'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(staffrole__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(staffrole__isnull=True)
        return queryset


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin panel configuration for UserProfile model."""
    list_display = ('user', 'profile_picture')
    inlines = [CustomerInline, ArtistInline, StaffRoleInline]
    list_filter = (IsCustomerFilter, IsArtistFilter, IsStaffFilter)
    search_fields = ('user__username', 'user__email')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin panel configuration for Customer model."""
    list_display = (
        'get_username',
        'receive_newsletter',
    )
    inlines = [AddressInline]
    search_fields = (
        'user_profile__user__username',
        'user_profile__user__email',
    )

    def get_username(self, obj):
        return obj.user_profile.user.username
    get_username.short_description = 'Username'


@admin.action(description="Approve selected artists")
def approve_artists(modeladmin, request, queryset):
    for artist in queryset:
        if not artist.is_approved:
            artist.is_approved = True
            artist.save()


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    """Admin panel configuration for Artist model."""
    list_display = (
        'get_username',
        'bio',
        'portfolio_url',
        'social_links',
        'is_approved',
        'approved_by',
        )
    search_fields = (
        'user_profile__user__username',
        'user_profile__user__email',
    )
    actions = [approve_artists]

    def get_username(self, obj):
        return obj.user_profile.user.username
    get_username.short_description = 'Username'


@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    """Admin panel configuration for StaffRole model."""
    list_display = ('get_username', 'role', 'created_at')
    search_fields = (
        'user_profile__user__username',
        'user_profile__user__email',
    )

    def get_username(self, obj):
        return obj.user_profile.user.username
    get_username.short_description = 'Username'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin panel configuration for Address model."""
    list_display = (
        'get_username',
        'label',
        'is_shipping',
        'is_billing',
        'first_name',
        'last_name',
        'address_line_1',
        'address_line_2',
        'postcode',
        'city',
        'country',
        'is_default'
    )
    list_filter = ('country', 'is_default', 'is_shipping', 'is_billing')
    search_fields = (
        'user_profile__user__username', 'city', 'country'
    )

    def get_username(self, obj):
        return obj.user_profile.user.username
    get_username.short_description = 'Username'
