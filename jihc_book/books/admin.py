from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Category, Author, Genre, Language, Book, RatingStar, Rating, Reviews
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BookAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Book
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "authors__name")  # фильтрация по категорию и автору фильма
    search_fields = ("title", "category__name")  # поиск по названию и категорию фильма
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ['publish', 'unpublish']
    form = BookAdminForm
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"), "year",)
        }),
        ("Авторы и Жанры", {
            "classes": ("collapse",),
            "fields": (("authors", "genres"),)
        }),
        ("Настройки", {
            "fields": (("url", "draft"),)
        }),
    )
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe('<img src={obj.poster.url} width="50" height="60">')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == '1':
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")


    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")


    publish.short_description = "Опубликовать"
    publish.allowed_permission = {'change', }

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permission = {'change', }


    get_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "book", "id")
    readonly_fields = ("name", "email")  # поля которые нельзя изменить в админке


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe('<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "book", "ip")


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


admin.site.register(RatingStar)

admin.site.site_title = "JIHC Books"
admin.site.site_header = "JIHC Books"
