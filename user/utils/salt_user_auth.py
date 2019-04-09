from rest_framework.throttling import SimpleRateThrottle


class UserGetCode(SimpleRateThrottle):
    scope = 'get_code'

    def get_cache_key(self, request, view):
        self.get_ident(request)
        return request.META.get('REMOTE_ADDR')