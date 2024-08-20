from typing import TypedDict

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

        numerator: int = 0
        denominator: int = 0

        for discipline in disciplines:

            ## validação da entrada
            try:
                if discipline['number_of_credits'] <= 0:
                    raise ValueError("O número de créditos da disciplina é menor ou igual a 0.")

                if not (self.semester_range['min'] <= discipline['semester'] <= self.semester_range['max']):
                    raise ValueError("O semestre está fora do intervalo delimitado entre 1 e 6.")

                if discipline['grade'] not in self.grade_map.keys():
                    raise ValueError("A menção não existe.")

            except TypeError:
                raise TypeError("O tipo de dado passado como parâmetro está incorreto.")


            ## cálculo do IRA
            numerator += self.grade_map[discipline['grade']] * \
                discipline['number_of_credits'] * \
                discipline['semester']


            denominator += discipline['number_of_credits'] * discipline['semester']

        return float(numerator / denominator)
            


