from drf_yasg import openapi
from requests import status_codes


class Errors():

    def __init__(self, erros: list[int]) -> None:
        self.erros = erros

    def get_schema(self) -> openapi.Schema:
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'errors': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Mensagem de erro'
                ),
            }
        )

    def retrieve_erros(self) -> dict[openapi.Response]:
        swagger_erros = dict()

        for error in self.erros:
            try:
                if str(error).startswith('4') or str(error).startswith('5'):
                    message = status_codes._codes[error][0].upper()
                    swagger_erros[error] = openapi.Response(
                        message, self.get_schema()
                    )
                else:
                    raise KeyError(f'Code {error} is not a valid HTTP error.')
            except KeyError:
                raise KeyError(
                    f'Code {error} not exists in HTTP status codes.')

        return swagger_erros
