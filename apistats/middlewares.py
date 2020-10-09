from time import time

from django.http import HttpRequest, HttpResponse

from .models import APIStat


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Call middleware
        :param request: HTTPRequest
        :return: HTTPResponse
        """
        start_time = time()
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        delay = time() - start_time
        APIStat.objects.create_from_request(
            request=request,
            delay=delay * 1000,
            status=response.status_code
        )
        return response
