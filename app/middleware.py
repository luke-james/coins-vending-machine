from django.http import JsonResponse
from django.urls import reverse

from vendingmachine.models import Machine


class MachineAuthMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path_info.startswith("/api") and request.path_info != reverse(
                "get_token") and request.path_info != reverse("create_machine"):
            token = request.META.get("AUTHORIZATION", request.META.get("HTTP_AUTHORIZATION", "")).replace("JWT ", "")

            if not token:
                return JsonResponse({"message": "JWT token required!"}, status=403)

            try:
                machine = Machine.objects.get(token=token)
            except Machine.DoesNotExist:
                return JsonResponse({"message": "Authentication required!"}, status=403)

            request.machine = machine
        response = self.get_response(request)
        return response
