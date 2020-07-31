#! /usr/bin/env python3
# coding: utf-8

"""
Author: [Nastyflav](https://github.com/Nastyflav) 2020-07-16
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

"""

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class ArtistsCatalogPage(Page):
    """Model of the artistes catalog"""
    subpage_types = ['ArtistPage']
    parent_page_types = ['home.HomePage']

    intro = RichTextField(blank=True)

    def get_context(self, request):
        """Update context to include only published artists, randomly ordered"""
        context = super().get_context(request)
        artists_pages = self.get_children().live().order_by('?')
        context['artists_pages'] = artists_pages
        return context

    class Meta:
        verbose_name = "Catalogue artistes"


class ArtistPage(Page):
    """All the fields to complete when editing an artist page"""
    subpage_types = []
    parent_page_types = ['ArtistsCatalogPage']

    style = models.CharField(max_length=100, verbose_name='Style')
    body = RichTextField(blank=True, verbose_name='Biographie')

    def main_image(self):
        """Print the artist image on top of the page"""
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('style'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('style'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
        InlinePanel('fb_link', label="Lien Facebook"),
        InlinePanel('insta_link', label="Lien Instagram"),
        InlinePanel('twitter_link', label="Lien Twitter"),
        InlinePanel('gigs', label="Concerts")
    ]

    class Meta:
        verbose_name = "Artiste"


class ArtistPageGalleryImage(Orderable):
    """Allows to integrate one image into an artiste page"""
    page = ParentalKey(ArtistPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]


class ArtistPageFacebookLink(Orderable):
    """Allows to integrate a Facebook link"""
    page = ParentalKey(ArtistPage, on_delete=models.CASCADE, related_name="fb_link")
    facebook = models.URLField(max_length=300, unique=True, null=True, verbose_name='Lien Facebook')

    panels = [
        FieldPanel('facebook'),
    ]


class ArtistPageInstagramLink(Orderable):
    """Allows to integrate a Facebook link"""
    page = ParentalKey(ArtistPage, on_delete=models.CASCADE, related_name="insta_link")
    instagram = models.URLField(max_length=300, unique=True, null=True, verbose_name='Lien Instagram')

    panels = [
        FieldPanel('instagram'),
    ]


class ArtistPageTwitterLink(Orderable):
    """Allows to integrate a Facebook link"""
    page = ParentalKey(ArtistPage, on_delete=models.CASCADE, related_name="twitter_link")
    twitter = models.URLField(max_length=300, unique=True, null=True, verbose_name='Lien Twitter')

    panels = [
        FieldPanel('twitter'),
    ]


class ArtistPageGigs(Orderable):
    """To add every gigs into the artist agenda"""
    page = ParentalKey(ArtistPage, on_delete=models.CASCADE, related_name="gigs")
    date = models.DateField(null=True, verbose_name="Date")
    city = models.CharField(max_length=100, null=True, verbose_name="Ville")
    location = models.CharField(max_length=300, null=True, verbose_name="Lieu")
    link = models.URLField(max_length=300, unique=True, null=True, verbose_name='Lien événement')

    panels = [
        FieldPanel('date'),
        FieldPanel('city'),
        FieldPanel('location'),
        FieldPanel('link'),
    ]