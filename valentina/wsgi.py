"""
WSGI config for valentina project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise


class DjangoCompressWhiteNoise(DjangoWhiteNoise):
    def __call__(self, environ, start_response):
        # Handle files generated on the fly by django-compressor
        url = environ['PATH_INFO']
        if url.startswith(self.static_prefix) and url not in self.files:
            if self.is_compressed_file(url):
                self.files[url] = self.find_file(url)

        return super().__call__(environ, start_response)

    def is_compressed_file(self, url):
        if not url.startswith(self.static_prefix):
            return False
        path = url[len(self.static_prefix):]
        return path.startswith(settings.COMPRESS_OUTPUT_DIR + "/")

    def is_immutable_file(self, path, url):
        if self.is_compressed_file(url):
            return True
        else:
            return super().is_immutable_file(path, url)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "valentina.settings")

application = DjangoCompressWhiteNoise(get_wsgi_application())
