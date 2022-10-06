from django.contrib import admin
from django.utils.html import format_html

from main_app.models import Film, Category, Comments


class FilmsAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
        except:
            pass
    list_display = ['image_tag', 'id', 'title', 'producer', 'rate', 'time',
                    'category']
    search_fields = 'title'.split()
    list_filter = 'category producer'.split()
    list_editable = 'category'.split()
    list_per_page = 5


admin.site.register(Film, FilmsAdmin)
admin.site.register(Category)
admin.site.register(Comments)


