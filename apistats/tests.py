from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory,TestCase

from .models import APIStat


class APIStatsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_create(self):
        request = self.factory.get('/test/a/path/')
        request.user = AnonymousUser()
        delay = 100
        status = 200
        apistat = APIStat.objects.create_from_request(request=request, delay=delay, status=status)
        self.assertIsNotNone(apistat)
        self.assertEqual(apistat.domain, 'test')
        self.assertEqual(apistat.path, '/test/a/path/')
        self.assertIsNone(apistat.user)
        self.assertEqual(apistat.delay, 100)
        self.assertEqual(apistat.status, 200)

    def test_create_without_user(self):
        request = self.factory.get('/test/a/path/')
        delay = 100
        status = 200
        apistat = APIStat.objects.create_from_request(request=request, delay=delay, status=status)
        self.assertIsNotNone(apistat)
        self.assertEqual(apistat.domain, 'test')
        self.assertEqual(apistat.path, '/test/a/path/')
        self.assertIsNone(apistat.user)
        self.assertEqual(apistat.delay, 100)
        self.assertEqual(apistat.status, 200)

    def test_create_with_user(self):
        request = self.factory.get('/test/a/path/')
        request.user = self.user
        delay = 100
        status = 200
        apistat = APIStat.objects.create_from_request(request=request, delay=delay, status=status)
        self.assertIsNotNone(apistat)
        self.assertEqual(apistat.domain, 'test')
        self.assertEqual(apistat.path, '/test/a/path/')
        self.assertIsNotNone(apistat.user)
        self.assertEqual(apistat.delay, 100)
        self.assertEqual(apistat.status, 200)

    def test_count(self):
        request_a = self.factory.get('/test/a/path/')
        request_b = self.factory.get('/test/b/path/')
        request_c = self.factory.get('/another/path/')
        request_a.user = AnonymousUser()
        request_b.user = AnonymousUser()
        request_c.user = AnonymousUser()
        delay = 100
        status = 200
        apistat_a = APIStat.objects.create_from_request(request=request_a, delay=delay, status=status)
        APIStat.objects.create_from_request(request=request_b, delay=delay+100, status=status)
        APIStat.objects.create_from_request(request=request_c, delay=delay+200, status=status)
        self.assertEqual(apistat_a.total_count(), 3)
        self.assertEqual(apistat_a.domain_count(), 2)
        self.assertEqual(apistat_a.path_count(), 1)

    def test_max_delay(self):
        request_a = self.factory.get('/test/a/path/')
        request_b = self.factory.get('/test/b/path/')
        request_c = self.factory.get('/another/path/')
        request_a.user = AnonymousUser()
        request_b.user = AnonymousUser()
        request_c.user = AnonymousUser()
        delay = 100
        status = 200
        apistat_a = APIStat.objects.create_from_request(request=request_a, delay=delay, status=status)
        APIStat.objects.create_from_request(request=request_b, delay=delay + 100, status=status)
        APIStat.objects.create_from_request(request=request_c, delay=delay + 200, status=status)
        self.assertEqual(apistat_a.max_delay(), 300)
        self.assertEqual(apistat_a.max_domain_delay(), 200)
        self.assertEqual(apistat_a.max_path_delay(), 100)

    def test_avg_delay(self):
        request_a = self.factory.get('/test/a/path/')
        request_b = self.factory.get('/test/b/path/')
        request_c = self.factory.get('/another/path/')
        request_a.user = AnonymousUser()
        request_b.user = AnonymousUser()
        request_c.user = AnonymousUser()
        delay = 100
        status = 200
        apistat_a = APIStat.objects.create_from_request(request=request_a, delay=delay, status=status)
        APIStat.objects.create_from_request(request=request_b, delay=delay + 100, status=status)
        APIStat.objects.create_from_request(request=request_c, delay=delay + 200, status=status)
        self.assertEqual(apistat_a.avg_delay(), 200)
        self.assertEqual(apistat_a.avg_domain_delay(), 150)
        self.assertEqual(apistat_a.avg_path_delay(), 100)




