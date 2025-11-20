from django.utils.deprecation import MiddlewareMixin


class DebugSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_key = request.session.session_key

    def process_response(self, request, response):
        session_key = request.session.session_key
        return response
