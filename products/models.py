# -*- coding: utf-8 -*-
import random, glob, os, shutil
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.conf import settings

from redactor.fields import RedactorField
from easy_thumbnails.fields import ThumbnailerImageField



type_choices = (
    (1, u'Sucata Inteira'),
    (2, u'Moto Documentada'),
    (3, u'Peça avulsa'),
)

state_choices = (
    ('SP', u'São Paulo'),
    ('RJ', u'Rio de Janeiro'),
)



class Brake(models.Model):
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = u"sistema de freio"
        verbose_name_plural = u"sistemas de freio"
        
    name = models.CharField(u'Nome', max_length=80)



class Mark(models.Model):
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = u"marca"
    
    name = models.CharField(u'Nome', max_length=80)



class Model(models.Model):
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = u"modelo"
    
    mark = models.ForeignKey(Mark, verbose_name=u"Marca")
    name = models.CharField(u'Nome', max_length=80)



class Photo(models.Model):
    class Meta:
        verbose_name = u"foto"
    
    def save(self):
        if self.image:
            if self.id:
                obj_photo = Photo.objects.get(id=self.id)
                if self.image not in [obj_photo.image]:
                    for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT,obj_photo.image)):
                        os.remove(fl)
            
            super(Photo, self).save()
    
    def delete(self):
        obj_photo = Photo.objects.get(id=self.id)
        super(Photo, self).delete()
        for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT,obj_photo.image)):
            os.remove(fl)
    
    def get_upload_to_image(self, filename):
        ext = filename[-3:].lower()
        if ext == 'peg': ext='jpeg'        
        return 'products/%s/%s_%s.%s' % (self.products.slug, datetime.now().strftime('%Y%m%d%H%M%S'), str(random.randint(00000,99999)), ext)
    
    def __unicode__(self):
        return u'%s' % self.image
    
    products = models.ForeignKey('Product')
    image = ThumbnailerImageField(u'Imagem', blank=True, upload_to = get_upload_to_image, resize_source=dict(size=(800, 600), sharpen=True, crop="scale"))
    title = models.CharField(u'Título', max_length=100, blank=True)
    main = models.BooleanField(u'Foto de capa')



class StartingSystem(models.Model):
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = u"sistema de partida"
        verbose_name_plural = u"sistemas de partida"
        
    name = models.CharField(max_length=40)



class ProductActivatedManager(models.Manager):
    def get_queryset(self):
        return super(ProductActivatedManager, self).get_queryset().filter(published=True).order_by('-banner_home','-updated_at')

class Product(models.Model):
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        verbose_name = u"produto"
    
    def save(self, *args, **kwargs):
        if not self.id:
            super(Product, self).save(*args, **kwargs)
            self.slug = slugify(str(self.id) + ' ' + self.title)
        super(Product, self).save(*args, **kwargs)
        
    def delete(self):
        slug = self.slug
        super(Product, self).delete()
        
        dir = '%s/products/%s' % (settings.MEDIA_ROOT, slug)
        
        if os.path.exists(dir):
            shutil.rmtree(dir)
    
    def clean(self):
        if not self.model.mark.id == self.mark.id:
            raise ValidationError(u'O Modelo selecionado não condiz com a Marca')
    
    def get_absolute_url(self):
        return reverse('products.views.details', kwargs={'slug': self.slug})
    
    def main_photo_set(self):
        photo = self.photo_set.order_by('-main','id')
        return photo[0] if photo else None
    
    brakes = models.ForeignKey(Brake, verbose_name=u"Sistema de Freio")
    starting_system = models.ForeignKey('StartingSystem', verbose_name=u"Sistema de Partida")
    mark = models.ForeignKey(Mark, verbose_name=u"Marca")
    model = models.ForeignKey(Model, verbose_name=u"Modelo")
    owner = models.ForeignKey(User, verbose_name=u"Usuário")
    
    type = models.IntegerField(u'Tipo', choices=type_choices)
    title = models.CharField(u'Título', max_length=160)
    slug = models.SlugField(max_length=200)
    video_link = models.URLField(u'Vídeo', max_length=160, blank=True, help_text=u"Informe o link do youtube")
    km = models.IntegerField()
    version = models.CharField(u'Versão', max_length=40, blank=True)
    year = models.IntegerField(u'Ano', blank=True, null=True)
    price = models.DecimalField(u'Preço', max_digits=6, decimal_places=2, blank=True, null=True)
    description = RedactorField(verbose_name=u'Descrição', allow_file_upload=False, allow_image_upload=False, blank=True)
    #description = models.TextField(u'Descrição', blank=True)
    state = models.CharField(u'Estado', max_length=4, blank=True,choices=state_choices)
    city = models.CharField(u'Cidade', max_length=120, blank=True)
    phone = models.CharField(u'Telefone', max_length=120, blank=True)
    used = models.BooleanField(u'Usado') # This field type is a guess.
    published = models.BooleanField(u'Publicado', default=True) # This field type is a guess.
    banner_home = models.BooleanField(u'Banner principal', default=False, help_text=u"Marque esta opção para que o produto apareça em posição de destaque no site")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    u''' Managers '''
    objects     = models.Manager()
    activated   = ProductActivatedManager()
