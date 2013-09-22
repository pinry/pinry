from __future__ import unicode_literals

from django.contrib.syndication.views import Feed
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django_images.models import Thumbnail
from taggit.models import Tag

from .models import Pin


def filter_generator_for(size):
    def wrapped_func(obj):
        return Thumbnail.objects.get_or_create_at_size(obj.pk, size)
    return wrapped_func


class LatestPins(Feed):
    title = 'Latest Pins'
    link = '/'
    description = 'The latest pins from around the internet.'

    domain_name = None

    item_enclosure_mime_type = 'image/jpeg'

    def get_object(self, request):
        """
        Doing this as a fix for Django's not including the domain name in
        enclosure urls.
        """
        try:
            request_type = 'http'
            if request.is_secure(): request_type = 'https'
            self.domain_name = ''.join([request_type, '://',
                                        get_current_site(request).domain])
        except:
            pass

    def items(self):
        return Pin.objects.order_by('-published')[:15]

    def item_pubdate(self, item):
        return item.published

    def item_link(self, item):
        return item.url

    def item_title(self, item):
        return item.url

    def item_description(self, item):
        tags = ', '.join(tag.name for tag in item.tags.all())
        return ''.join(['Description: ', item.description or 'None',
                        ' | Tags: ', tags or 'None'])

    def item_enclosure_url(self, item):
        slug = unicode(filter_generator_for('standard')(item.image).image.url)
        return self.domain_name + slug

    def item_enclosure_length(self, item):
        return filter_generator_for('standard')(item.image).image.size


class LatestUserPins(Feed):
    description = 'The latest pins from around the internet.'

    domain_name = None

    item_enclosure_mime_type = 'image/jpeg'

    def get_object(self, request, user):
        """
        Doing this as a fix for Django's not including the domain name in
        enclosure urls.
        """
        request_type = 'http'
        if request.is_secure(): request_type = 'https'
        self.domain_name = ''.join([request_type, '://',
                                    get_current_site(request).domain])
        return get_object_or_404(User, username=user)

    def title(self, obj):
        return 'Latest Pins from ' + obj.username

    def link(self, obj):
        return '/pins/user/' + obj.username + '/'

    def items(self, obj):
        return Pin.objects.filter(submitter=obj).order_by('-published')[:15]

    def item_pubdate(self, item):
        return item.published

    def item_link(self, item):
        return item.url

    def item_title(self, item):
        return item.url

    def item_description(self, item):
        tags = ', '.join(tag.name for tag in item.tags.all())
        return ''.join(['Description: ', item.description or 'None',
                        ' | Tags: ', tags or 'None'])

    def item_enclosure_url(self, item):
        slug = unicode(filter_generator_for('standard')(item.image).image.url)
        return self.domain_name + slug

    def item_enclosure_length(self, item):
        return filter_generator_for('standard')(item.image).image.size


class LatestTagPins(Feed):
    link = '/'
    description = 'The latest pins from around the internet.'

    domain_name = None

    item_enclosure_mime_type = 'image/jpeg'

    def get_object(self, request, tag):
        """
        Doing this as a fix for Django's not including the domain name in
        enclosure urls.
        """
        request_type = 'http'
        if request.is_secure(): request_type = 'https'
        self.domain_name = ''.join([request_type, '://',
                                    get_current_site(request).domain])
        return get_object_or_404(Tag, name=tag)

    def title(self, obj):
        return 'Latest Pins in ' + obj.name

    def link(self, obj):
        return '/pins/tag/' + obj.name + '/'

    def items(self, obj):
        return Pin.objects.filter(tags=obj).order_by('-published')[:15]

    def item_pubdate(self, item):
        return item.published

    def item_link(self, item):
        return item.url

    def item_title(self, item):
        return item.url

    def item_description(self, item):
        tags = ', '.join(tag.name for tag in item.tags.all())
        return ''.join(['Description: ', item.description or 'None',
                        ' | Tags: ', tags or 'None'])

    def item_enclosure_url(self, item):
        slug = unicode(filter_generator_for('standard')(item.image).image.url)
        return self.domain_name + slug

    def item_enclosure_length(self, item):
        return filter_generator_for('standard')(item.image).image.size

