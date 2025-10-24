

# gpt/views.py
import threading
import atexit
from django.http import HttpResponse
from django.template import loader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .local_api import LOCAL_API

local_api_instance = LOCAL_API()
_local_api_lock = threading.Lock()

def _shutdown_local_api():
    try:
        local_api_instance.quit_driver()
        del local_api_instance
    except Exception:
        pass

atexit.register(_shutdown_local_api)


class LocalAPIView(APIView):
    """
    GET /api/local/?prompt=... 
    Example: /api/local/?prompt=what%20is%2033*88
    """
    def get(self, request, *args, **kwargs):
        prompt = request.query_params.get("prompt")

        # If no prompt → render HTML page with message box
        if not prompt:
            template = loader.get_template("local_api.html")
            return HttpResponse(template.render({}, request))

        # Otherwise → process request normally
        acquired = _local_api_lock.acquire(timeout=300)
        if not acquired:
            return Response({"Error": "Server busy, try again later"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            # Call the method that interacts with selenium
            # Optionally pass timeout params via query params, e.g. ?timeout=20
            timeout = request.query_params.get("timeout")
            try:
                timeout = float(timeout) if timeout is not None else None
            except ValueError:
                timeout = None

            # If your LOCAL_API.execute_prompt accepts timeout parameters use them.
            if timeout is not None:
                print(f"Executing prompt with timeout={timeout}")
                result = local_api_instance.execute_prompt(prompt, timeout=timeout)
            else:
                print("Executing prompt with default timeout")
                result = local_api_instance.execute_prompt(prompt)

            return Response({"result": result}, status=status.HTTP_200_OK)
        except Exception as e:
            local_api_instance.restart_driver()
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            _local_api_lock.release()
