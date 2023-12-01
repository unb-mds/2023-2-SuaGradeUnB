from typing import Any
from argparse import ArgumentParser as CommandParser
from django.core.management.base import BaseCommand
from utils import sessions, web_scraping
from utils.db_handler import delete_classes_from_discipline, delete_all_departments_using_year_and_period, get_or_create_department, get_or_create_discipline, create_class
from time import time


class Command(BaseCommand):
    """Comando para atualizar o banco de dados."""

    help = "Atualiza o banco de dados com as disciplinas do SIGAA e suas respectivas turmas."

    def add_arguments(self, parser: CommandParser) -> None:
        """Adiciona os argumentos do comando."""
        parser.add_argument('-a', '-all', action='store_true', dest='all', default=False,
                            help="Atualiza o banco de dados com as disciplinas dos períodos atual e seguinte.")

        parser.add_argument('-p', '--period', action='store', default=None,
                            choices=[".".join(sessions.get_current_year_and_period()), ".".join(
                                sessions.get_next_period())],
                            dest='period', help="Atualiza o banco de dados com as disciplinas do período especificado.")

        parser.add_argument('-d', '--delete', action='store_true', dest='delete', default=False,
                            help="Deleta o período especificado do banco de dados.")

    def handle(self, *args: Any, **options: Any):
        choices = []

        if options["all"]:
            choices.append(sessions.get_current_year_and_period())
            choices.append(sessions.get_next_period())
        elif options["period"] is not None:
            choices.append(options["period"].split("."))
        else:
            print("Nenhum período foi especificado.")
            print("Utilize o comando 'updatedb -h' para mais informações.")
            return

        # Obtem o ano e o período anterior ao período atual
        previous_period_year, previous_period = sessions.get_previous_period()

        # Apaga as disciplinas do período anterior
        delete_all_departments_using_year_and_period(
            year=previous_period_year, period=previous_period)

        if options["delete"]:
            for year, period in choices:
                self.delete_period(year=year, period=period)
            return

        departments_ids = web_scraping.get_list_of_departments()

        if departments_ids is None:
            self.display_error_message("department_ids")
            return

        print("Atualizando o banco de dados...")

        for year, period in choices:
            try:
                start_time = time()
                self.update_departments(
                    departments_ids=departments_ids, year=year, period=period)
                self.display_success_update_message(
                    operation=f"{year}/{period}", start_time=start_time)
            except Exception as exception:
                print("Houve um erro na atualização do bando de dados.")
                print(f"Error: {exception}")

    def update_departments(self, departments_ids: list, year: str, period: str) -> None:
        """Atualiza os departamentos do banco de dados e suas respectivas disciplinas."""
        for department_id in departments_ids:
            print(f"WebScraping do departamento: {department_id}")
            disciplines_list = web_scraping.get_department_disciplines(
                department_id=department_id, current_year=year, current_period=period)
            department = get_or_create_department(
                code=department_id, year=year, period=period)

            print("Atualizando disciplinas do departamento...")
            # Para cada disciplina do período atual, deleta as turmas previamente cadastradas e cadastra novas turmas no banco de dados
            for discipline_code in disciplines_list:
                classes_info = disciplines_list[discipline_code]
                # Cria ou pega a disciplina
                discipline = get_or_create_discipline(
                    name=classes_info[0]["name"], code=discipline_code, department=department)

                # Deleta as turmas previamente cadastradas
                delete_classes_from_discipline(discipline=discipline)

                # Cadastra as novas turmas
                for class_info in classes_info:
                    create_class(teachers=class_info["teachers"],
                                 classroom=class_info["classroom"], schedule=class_info["schedule"],
                                 days=class_info["days"], _class=class_info["class_code"], discipline=discipline, special_dates=class_info["special_dates"])

    def delete_period(self, year: str, period: str) -> None:
        """Deleta um período do banco de dados."""
        start_time = time()
        delete_all_departments_using_year_and_period(year=year, period=period)
        self.display_success_delete_message(
            operation=f"{year}/{period}", start_time=start_time)

    def display_error_message(self, operation: str) -> None:
        print("Não foi possível realizar a operação de atualização do banco de dados.")
        print("Verifique se o SIGAA está funcionando corretamente.")
        print(f"Falha em {operation}\n")

    def display_success_update_message(self, operation: str, start_time: float) -> None:
        print("Operação de atualização do banco de dados realizada com sucesso.")
        print(f"Sucesso em {operation}")
        print(f"Tempo de execução: {(time() - start_time):.1f}s\n")

    def display_success_delete_message(self, operation: str, start_time: float) -> None:
        print("Operação de remoção do banco de dados realizada com sucesso.")
        print(f"Sucesso em {operation}")
        print(f"Tempo de execução: {(time() - start_time):.1f}s\n")
