from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class DebugSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_key = request.session.session_key
        logger.debug(f"Session key: {session_key}")
        logger.debug(
            f"Session data before processing: {list(request.session.items())}"
        )

    def process_response(self, request, response):
        session_key = request.session.session_key
        logger.debug(f"Session key after processing: {session_key}")
        logger.debug(
            f"Session data after processing: {list(request.session.items())}"
        )
        return response
