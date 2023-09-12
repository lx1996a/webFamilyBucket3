from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        if request.path_info in ["/login/","/image/code/"]:
            return

        info = request.session.get("info")
        # print(info)
        if info:
            return

        return redirect("/login/")