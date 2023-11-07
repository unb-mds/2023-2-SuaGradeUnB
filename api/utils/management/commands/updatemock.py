from typing import Any
from utils.sessions import get_response, create_request_session
from django.core.management.base import BaseCommand
from pathlib import Path
import os


class Command(BaseCommand):
    """Comando para atualizar os arquivos de mock do SIGAA."""

    help = "Atualiza os arquivos do mock com as informações do SIGAA requisitadas."

    def handle(self, *args: Any, **options: Any):
        current_path = Path(__file__).parent.parent.parent.absolute()

        os.remove(current_path / "mock/departments.html")
        with open(current_path / "mock/departments.html", "a") as mockfile:
            response = get_response(create_request_session())
            encoding = response.encoding if response.encoding else 'utf-8'

            mockfile.write(response.content.decode(encoding))
