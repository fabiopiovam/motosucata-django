# -*- coding: utf-8 -*-

from products.models import *
from django.contrib import admin
from flexselect import FlexSelectWidget

class MarkModelWidget(FlexSelectWidget):
    """
    The widget must extend FlexSelectWidget and implement trigger_fields, 
    details(), queryset() and empty_choices_text().
    """

    trigger_fields = ['mark']
    """Fields which on change will update the base field."""

    def queryset(self, instance):
        """
        Returns the QuerySet populating the base field. If either of the
        trigger_fields is None, this function will not be called.

        - instance: A partial instance of the parent model loaded from the
                    request.
        """
        mark = instance.mark.id
        
        return Model.objects.filter(mark=mark)

    def empty_choices_text(self, instance):
        """
        If either of the trigger_fields is None this function will be called
        to get the text for the empty choice in the select box of the base
        field.

        - instance: A partial instance of the parent model loaded from the
                    request.
        """
        return ""
    
    def details(self, base_field_instance, instance):
        return u""

class PhotoInline(admin.TabularInline):
    template = 'admin/tabular_image.html'
    model = Photo
    extra = 1
    fields = ['image','main','title']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'owner', 'mark', 'model', 'published')
    list_filter = ['published','type','mark__name']
    search_fields = ['title','slug','mark__name','model__name', 'owner__username']
    
    fieldsets = [
        (None,                      {'fields': ['type','mark','model','version','year','km','brakes','starting_system','price','used']}),
        (u'Localização do veículo', {'fields': ['city','state']}),
        (u'Dados para contatos',    {'fields': ['phone']}),
        (u'Dados para publicação',  {'fields': ['title','video_link','description','published']}),
    ]
    
    inlines = [PhotoInline]
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner_id', None) is None:
            obj.owner_id = request.user.id
        obj.save()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Alters the widget displayed for the base field.
        """
        if db_field.name == "model":
            kwargs['widget'] =  MarkModelWidget(
                base_field=db_field,
                modeladmin=self,
                request=request,
            )
            
        return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ModelAdmin(admin.ModelAdmin):
    list_display = ('name','mark')
    search_fields = ['name']
    list_filter = ['mark__name']

admin.site.register(Product,ProductAdmin)
admin.site.register(Brake)
admin.site.register(Mark)
admin.site.register(Model,ModelAdmin)
admin.site.register(StartingSystem)