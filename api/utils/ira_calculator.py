from typing import TypedDict
import inspect

class Discipline(TypedDict):
    """
    TypedDict que define uma disciplina.

    Attributes:
        grade: a menção obtida pelo aluno na disciplina.
        number_of_credits: a quantidade de créditos que a disciplina tem.
        semester: qual o semestre em que o aluno realizou a disciplina. O valor mínimo é 1, e o máximo é 6.
    """

    grade: str
    number_of_credits: int
    semester: int


# Validação dos tipos da entrada
def validate(func):
    def wrapper(self, *args, **kwargs):
        members = inspect.getmembers(Discipline, lambda x: not inspect.isroutine(x))
        attributes = set()

        for key, value in members:
            if key == "__annotations__":
                for var_name, var_type in value.items():
                    attributes.add((var_name, var_type))

        values = args[0] if len(args) else kwargs["disciplines"]
        for value in values:
            for attr_name, attr_type in attributes:
                result = value.get(attr_name, None)

                if not isinstance(result, attr_type):
                    raise TypeError(
                        f"O valor de '{attr_name}' deve ser do tipo '{attr_type.__name__}'."
                    )

                if isinstance(result, int) and result <= 0:
                    raise ValueError(
                        f"O valor de '{attr_name}' deve ser maior que zero."
                    )

        return func(self, *args, **kwargs)

    return wrapper


class IraCalculator:
    """
    Classe que calcula o valor do IRA a partir de um conjunto de disciplinas.

    Atualmente, o cálculo está sendo baseado com base no
     recurso do seguinte link: 'https://deg.unb.br/images/legislacao/resolucao_ceg_0001_2020.pdf'

    Para uma disciplina, nos interessam as seguintes variáveis:
    E -> Equivalência da menção de disciplina (isto é, SS=5, MS=4,..., SR=0);
    C -> Número de créditos daquela disciplina;
    S -> Semestre em que aquela disciplina foi cursada, sendo 6 o seu valor máximo.

    Realiza-se o somatório de E*C*S para cada disciplina, e depois divide-se pelo somatório de C*S para cada uma delas.
    """

    def __init__(self) -> None:
        self.grade_map = {
            "SS": 5,
            "MS": 4,
            "MM": 3,
            "MI": 2,
            "II": 1,
            "SR": 0,
        }

        self.semester_range = {
            "min": 1,
            "max": 6,
        }

    def get_grade_number(self, grade: str):
        return self.grade_map.get(grade.upper(), None)

    @validate
    def get_ira_value(self, disciplines: list[Discipline]) -> float:
        """
        Obter o valor do IRA a partir de um conjunto de menções.
        :param disciplines: A lista de disciplinas que um aluno pegou.

        :returns: Um float com o valor calculado do IRA.
        """

        numerator: int = 0
        denominator: int = 0

        for discipline in disciplines:
            # Para o cálculo do IRA, o maior valor possível para semestre é 6, mesmo
            # que o estudante esteja num semestre maior que esse
            grade: str = discipline.get("grade")
            semester: int = discipline.get("semester")
            number_of_credits: int = discipline.get("number_of_credits")

            semester = min(
                semester, self.semester_range["max"]
            )

            grade_number = self.get_grade_number(grade)
            if grade_number is None:
                raise ValueError(f"A menção {grade} não existe.")

            ## Cálculo do IRA
            numerator += (
                grade_number * number_of_credits * semester
            )

            denominator += number_of_credits * semester

        return float(numerator / denominator)
