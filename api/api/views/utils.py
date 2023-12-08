from rest_framework import status, response


def handle_400_error(error_msg: str) -> response.Response:
    return response.Response(
        {
            "errors": error_msg
        }, status.HTTP_400_BAD_REQUEST)
