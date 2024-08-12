from typing import TypedDict

class Discipline(TypedDict):
    """
    TypedDict que define uma disciplina.
    
    Attributes:
        mencao: a menção obtida pelo aluno na disciplina.
        qtd_creditos: a quantidade de créditos que a disciplina tem.
        semestre: qual o semestre em que o aluno realizou a disciplina. O valor mínimo é 1, e o máximo é 6. 
    """
    mencao: str
    qtd_creditos: int
    semestre: int

class IraCalculator:
    """
    Classe que calcula o valor do IRA a partir de um conjunto de disciplinas.
    """

    def __init__(self) -> None:
        self.mencaoMap = {
            'SS': 5,
            'MS': 4,
            'MM': 3,
            'MI': 2,
            'II': 1,
            'SR': 0,
        }

        self.semester_range = {
            'min': 1,
            'max': 6,
        }

    def get_ira_value(self, disciplines: list[Discipline]) -> float:
        """
        Obter o valor do IRA a partir de um conjunto de menções.
        :param disciplines: A lista de disciplinas que um aluno pegou. 

        :returns: Um float com o valor calculado do IRA.
        """

        numerador: int = 0
        denominador: int = 0

        for discipline in disciplines:

            if not (self.semester_range['min'] <= discipline['semestre'] <= self.semester_range['max']):
                raise ValueError("O semestre está fora do intervalo delimitado entre 1 e 6.")

            if discipline['mencao'] not in self.mencaoMap.keys():
                raise ValueError("A menção não existe.")

            numerador += self.mencaoMap[discipline['mencao']] * \
                discipline['qtd_creditos'] * \
                discipline['semestre']

            denominador += discipline['qtd_creditos'] * discipline['semestre']

        return float(numerador)/float(denominador)
            


