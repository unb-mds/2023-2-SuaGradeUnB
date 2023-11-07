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
        parser.add_argument('-rc', '--remove-current-period', action='store_false', default=True,
                            dest='current_period', help="Ativa ou desativa sistema para atualização do período atual.")
        parser.add_argument('-rn', '--remove-next-period', action='store_false', default=True,
                            dest='next_period', help="Ativa ou desativa sistema para atualização do próximo período.")

        parser.add_argument('-dc', '--delete-current-period', action='store_true', default=False,
                            dest='delete_current_period', help="Deleta o período atual do banco de dados")
        parser.add_argument('-dn', '--delete-next-period', action='store_true', default=False,
                            dest='delete_next_period', help="Deleta o próximo período do banco de dados")

    def handle(self, *args: Any, **options: Any):
        current_period_enabled = options["current_period"]
        next_period_enabled = options["next_period"]
        delete_current_period = options["delete_current_period"]
        delete_next_period = options["delete_next_period"]

        if not current_period_enabled and not next_period_enabled:
            self.stderr.write(
                "Nenhum período foi selecionado para atualização.")
            return

        departments_ids = web_scraping.get_list_of_departments()

        if departments_ids is None:
            self.display_error_message("department_ids")
            return

        print("Atualizando o banco de dados...\n")

        # Obtem o ano e o período atual e o ano e o período seguinte
        previous_period_year, previous_period = sessions.get_previous_period()

        # Apaga as disciplinas do período interior
        delete_all_departments_using_year_and_period(
            previous_period_year, previous_period)
        if not delete_current_period and not delete_next_period:
            if current_period_enabled:
                # Atualiza as disciplinas do período atual
                start_time = time()
                current_year, current_period = sessions.get_current_year_and_period()
                self.update_departments(
                    departments_ids=departments_ids, year=current_year, period=current_period)
                self.display_success_update_message(
                    operation=f"{current_year}/{current_period}", start_time=start_time)

            if next_period_enabled:
                # Atualiza as disciplinas do período seguinte
                start_time = time()
                next_period_year, next_period = sessions.get_next_period()
                self.update_departments(
                    departments_ids=departments_ids, year=next_period_year, period=next_period)
                self.display_success_update_message(
                    operation=f"{next_period_year}/{next_period}", start_time=start_time)

        elif delete_current_period and delete_next_period:
            # Deleta ambos os períodos
            start_time = time()
            current_year, current_period = sessions.get_current_year_and_period()
            next_period_year, next_period = sessions.get_next_period()
            self.display_deleting_message(
                operation=f"{current_year}/{current_period} and {next_period_year}/{next_period}")
            delete_all_departments_using_year_and_period(
                year=current_year, period=current_period)
            delete_all_departments_using_year_and_period(
                year=next_period_year, period=next_period)
            self.display_success_delete_message(
                operation=f"{current_year}/{current_period} and {next_period_year}/{next_period}", start_time=start_time)
            return
        elif delete_current_period:
            # Deleta o período atual
            start_time = time()
            current_year, current_period = sessions.get_current_year_and_period()
            self.display_deleting_message(
                operation=f"{current_year}/{current_period}")
            delete_all_departments_using_year_and_period(
                year=current_year, period=current_period)
            self.display_success_delete_message(
                operation=f"{current_year}/{current_period}", start_time=start_time)
            return
        else:
            # Deleta o período seguinte
            start_time = time()
            next_period_year, next_period = sessions.get_next_period()
            self.display_deleting_message(
                operation=f"{next_period_year}/{next_period}")
            delete_all_departments_using_year_and_period(
                year=next_period_year, period=next_period)
            self.display_success_delete_message(
                operation=f"{next_period_year}/{next_period}", start_time=start_time)
            return

    def update_departments(self, departments_ids: list, year: str, period: str) -> None:
        """Atualiza os departamentos do banco de dados e suas respectivas disciplinas."""
        for department_id in departments_ids:
            disciplines_list = web_scraping.get_department_disciplines(
                department_id=department_id, current_year=year, current_period=period)
            department = get_or_create_department(
                code=department_id, year=year, period=period)
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
                    create_class(workload=class_info["workload"], teachers=class_info["teachers"],
                                 classroom=class_info["classroom"], schedule=class_info["schedule"],
                                 days=class_info["days"], _class=class_info["class_code"], discipline=discipline)

    def display_error_message(self, operation: str) -> None:
        self.stdout.write(self.style.ERROR(
            "Não foi possível realizar a operação de atualização do banco de dados."))
        self.stdout.write(self.style.ERROR(
            "Verifique se o SIGAA está funcionando corretamente."))
        self.stdout.write(self.style.ERROR(f"Falha em {operation}\n\n"))

    def display_success_update_message(self, operation: str, start_time: float) -> None:
        self.stdout.write(self.style.SUCCESS(
            "Operação de atualização do banco de dados realizada com sucesso."))
        self.stdout.write(self.style.SUCCESS(f"Sucesso em {operation}"))
        self.stdout.write(self.style.SUCCESS(
            f"Tempo de execução: {(time() - start_time):.1f}s\n\n"))

    def display_success_delete_message(self, operation: str, start_time: float) -> None:
        self.stdout.write(self.style.SUCCESS(
            "Operação de remoção do banco de dados realizada com sucesso."))
        self.stdout.write(self.style.SUCCESS(f"Sucesso em {operation}"))
        self.stdout.write(self.style.SUCCESS(
            f"Tempo de execução: {(time() - start_time):.1f}s\n\n"))

    def display_deleting_message(self, operation: str) -> None:
        self.stdout.write(
            "Operação de remoção do banco de dados iniciada.")
        self.stdout.write(f"Deletando {operation}...\n\n")
