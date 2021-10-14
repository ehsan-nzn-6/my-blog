from blog.models import IPAddress


class SaveIPAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        ip = self.get_client_ip(request)
        self.ip_is_exist_or_save(request, ip)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # its better than else
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def ip_is_exist_or_save(self, request, ip):
        try:
            ip_address = IPAddress.objects.get(ip_address=ip)
        except IPAddress.DoesNotExist:
            ip_address = IPAddress(ip_address=ip)
            ip_address.save()
        request.user.ip_address = ip_address
