from  django.contrib.sitemaps import Sitemap
from mint_app.models import MModel


class MModelSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return MModel.objects.all()

    def lastmod(self, obj):
        pass
