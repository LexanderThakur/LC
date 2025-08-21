from django.http import JsonResponse

from ..accounts.models import Session

class AuthMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        token=request.headers.get("Authorization")

        request.user=None

        if token:
            session=Session.objects.filter(token=token).select_related("user_email").first()

            if session:
                request.user=session.user_email

        return self.get_response(request)


