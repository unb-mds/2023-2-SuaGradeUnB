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

    def add_error(self, swagger_erros: dict[openapi.Response], error: int, key_error: KeyError):
        check_error = str(error).startswith('4') or str(error).startswith('5')
        if check_error:
            message = status_codes._codes[error][0].upper()
            swagger_erros[error] = openapi.Response(message, self.get_schema())
        else:
            raise key_error

    def retrieve_erros(self) -> dict[openapi.Response]:
        swagger_erros = dict()

        for error in self.erros:
            key_error = KeyError(f'Code {error} is not a valid HTTP error.')

            try:
                self.add_error(swagger_erros, error, key_error)
            except KeyError:
                raise key_error

        return swagger_erros
