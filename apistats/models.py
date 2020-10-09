from django.contrib.auth.models import User
from django.db import models
from django.http import HttpRequest
from django.conf import settings

class APIStat:
    pass


class APIStatManager(models.Manager):

    def create_from_request(
            self,
            request: HttpRequest,
            delay: int = 0,
            status: int = 200
    ) -> (APIStat, None):
        excluded_domains = getattr(settings, 'APISTAT_EXCLUDED_DOMAINS', frozenset())
        domain = self._get_domain(request.path_info)
        if domain in excluded_domains:
            return
        apistat = APIStat()
        apistat.method = request.method
        apistat.query = request.META.get('QUERY_STRING')
        apistat.path = request.path_info
        apistat.domain = domain
        apistat.delay = delay
        apistat.status = status
        apistat.ip = request.headers.get('X-Real-IP', request.META.get('REMOTE_ADDR'))
        apistat.user = request.user if request.user.is_authenticated else None
        apistat.save()

    def _get_domain(self, path):
        split_path = path.split('/')
        if len(split_path) >= 2:
            return split_path[1]
        else:
            return ''


class APIStat(models.Model):
    record_time = models.DateTimeField("Recorded at", auto_now=True, primary_key=True)
    method = models.CharField("call method", max_length=10)
    domain = models.CharField("Application domain", max_length=50, db_index=True)
    path = models.CharField("Application path", max_length=255, db_index=True)
    query = models.CharField("Query parameters", max_length=2000, blank=True)
    ip = models.GenericIPAddressField("Client IP address", null=True, blank=True)
    delay = models.IntegerField("delay (ms) between request and response")
    status = models.IntegerField("Response status code")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    objects = APIStatManager()

    @property
    def record_month(self):
        return self.record_time.strftime('%Y-%M')

    @classmethod
    def total_count(cls):
        return cls.objects.count()

    def path_count(self):
        return APIStat.objects.filter(path=self.path).count()

    def domain_count(self):
        return APIStat.objects.filter(domain=self.domain).count()

    def avg_path_delay(self):
        return APIStat.objects.filter(path=self.path).aggregate(avg_delay=models.Avg('delay')).get('avg_delay', 0)

    def avg_domain_delay(self):
        return APIStat.objects.filter(domain=self.domain).aggregate(avg_delay=models.Avg('delay')).get('avg_delay', 0)

    @classmethod
    def max_delay(cls):
        return cls.objects.aggregate(max_delay=models.Max('delay')).get('max_delay', 0)

    def max_path_delay(self):
        return APIStat.objects.filter(path=self.path).aggregate(max_delay=models.Max('delay')).get('max_delay', 0)

    def max_domain_delay(self):
        return APIStat.objects.filter(domain=self.domain).aggregate(max_delay=models.Max('delay')).get('max_delay', 0)

    @classmethod
    def avg_delay(cls):
        return cls.objects.aggregate(avg_delay=models.Avg('delay')).get('avg_delay', 0)

    class Meta:
        ordering = ['-record_time', 'path']
        get_latest_by = ['-record_time', 'path']
