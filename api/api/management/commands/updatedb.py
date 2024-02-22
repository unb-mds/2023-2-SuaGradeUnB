from typing import Any
from argparse import ArgumentParser as CommandParser
from django.core.management.base import BaseCommand
from django.db import transaction
from utils import sessions
from utils import db_handler as dbh
from utils.web_scraping import DisciplineWebScraper, get_list_of_departments
from django.core.cache import cache
from time import time, sleep
from collections import deque
from core.settings.base import THIRTY_DAYS_IN_SECS
import threading


class Command(BaseCommand):
    """Comando para atualizar o banco de dados."""

    help = "Atualiza o banco de dados com as disciplinas do SIGAA e suas respectivas turmas."

    def add_arguments(self, parser: CommandParser) -> None:
        """Adiciona os argumentos do comando."""
        parser.add_argument('-a', '--all', action='store_true', dest='all', default=False,
                            help="Atualiza o banco de dados com as disciplinas dos períodos atual e seguinte.")

        parser.add_argument('-ds', '--descriptive', action='store_true', default=False,
                            help="Ativa a opção de uma atualização descritiva com os outputs (print) necessários")

        parser.add_argument('-p', '--period', action='store', default=None,
                            choices=[".".join(sessions.get_current_year_and_period()), ".".join(
                                sessions.get_next_period())],
                            dest='period', help="Atualiza o banco de dados com as disciplinas do período especificado.")

        parser.add_argument('-d', '--delete', action='store_true', dest='delete', default=False,
                            help="Deleta o período especificado do banco de dados.")

    def handle(self, *args: Any, **options: Any):
        choices = []
        threads = []

        if options["all"]:
            choices.append(sessions.get_current_year_and_period())
            choices.append(sessions.get_next_period())
        elif options["period"] is not None:
            choices.append(options["period"].split("."))
        else:
            print("Nenhum período foi especificado.")
            print("Utilize o comando 'updatedb -h' para mais informações.")
            return

        # Obtém o ano e o período anterior ao período atual
        previous_period_year, previous_period = sessions.get_previous_period()

        # Apaga as disciplinas do período anterior
        dbh.delete_all_departments_using_year_and_period(
            year=previous_period_year, period=previous_period)

        if options["delete"]:
            for year, period in choices:
                thread = threading.Thread(
                    target=self.delete_period, args=(year, period,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
            threads.clear()

            return

        departments_data = get_list_of_departments()
        if departments_data is None:
            self.display_error_message("get_list_of_departments")
            return
        departments_ids, departments_names = departments_data
        if departments_ids is None or departments_names is None:
            self.display_error_message("get_list_of_departments")

        print("Atualizando o banco de dados...")

        def start_update_year_period(year: str, period: str):
            try:
                start_time = time()
                print(f"Começando atualização de {year}/{period}")
                with transaction.atomic():
                    self.update_departments(
                        departments_ids=departments_ids, departments_names=departments_names, year=year, period=period, options=options)

                self.display_success_update_message(
                    operation=f"{year}/{period}", start_time=start_time)
            except Exception as exception:
                print("Houve um erro na atualização do banco de dados.")
                print(f"Error: {exception}")

        start_tot_time = time()
        for year, period in choices:
            thread = threading.Thread(
                target=start_update_year_period, args=(year, period,))
            threads.append(thread)
            thread.start()
            sleep(0.01)  # little time to start print don't overleap

        print()

        for thread in threads:
            thread.join()
        threads.clear()

        print(f"\nTempo total de execução: {(time() - start_tot_time):.1f}s")

    def update_departments(self, departments_ids: list, departments_names: list, year: str, period: str, options: Any) -> None:
        """Atualiza os departamentos do banco de dados e suas respectivas disciplinas."""
        def execute_update(department_id, department_name) -> None:
            scraper = DisciplineWebScraper(department_id, year, period)
            fingerprint = scraper.create_page_fingerprint()

            cache_key = f"{department_id}/{year}.{period}"
            try:
                cache_value = cache.get(cache_key)
                if cache_value and cache_value == fingerprint:
                    if options['descriptive']:
                        print(f"Departamento ({department_id}) atualizado, operação não necessária")
                    return
            except:
                print("Ocorreu um erro ao tentar acessar o cache")
                pass

            disciplines_list = scraper.get_disciplines()
            department = dbh.get_or_create_department(
                code=department_id, name=department_name, year=year, period=period)

            if options['descriptive']:
                print(f"Departamento ({department_id}) desatualizado, operação necessária")

            # Para cada disciplina do período atual, deleta as turmas previamente cadastradas e cadastra novas turmas no banco de dados
            for discipline_code in disciplines_list:
                classes_info = disciplines_list[discipline_code]
                # Cria ou pega a disciplina
                discipline = dbh.get_or_create_discipline(
                    name=classes_info[0]["name"], code=discipline_code, department=department)

                # Deleta as turmas previamente cadastradas
                dbh.delete_classes_from_discipline(discipline=discipline)

                # Cadastra as novas turmas
                for class_info in classes_info:
                    dbh.create_class(teachers=class_info["teachers"],
                                     classroom=class_info["classroom"], schedule=class_info["schedule"],
                                     days=class_info["days"], _class=class_info["class_code"], discipline=discipline, special_dates=class_info["special_dates"])

            cache.set(cache_key, fingerprint, timeout=THIRTY_DAYS_IN_SECS)

            if options['descriptive']:
                print(f'Operação de atualização finalizada para o departamento ({department_id})')

        threads = deque()
        for department_id, department_name in zip(departments_ids, departments_names):
            thread = threading.Thread(
                target=execute_update, args=(department_id, department_name))
            threads.append(thread)
            thread.start()

            if len(threads) == 3:
                threads[0].join()
                threads.popleft()

        for thread in threads:
            thread.join()
        threads.clear()

    def delete_period(self, year: str, period: str) -> None:
        """Deleta um período do banco de dados."""
        start_time = time()
        with transaction.atomic():
            dbh.delete_all_departments_using_year_and_period(
                year=year, period=period)
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
