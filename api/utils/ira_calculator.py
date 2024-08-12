class IraCalculator:
    def __init__(self) -> None:
        self.mencaoMap = {
            'SS': 5,
            'MS': 4,
            'MM': 3,
            'MI': 2,
            'II': 1,
            'SR': 0,
        }

        """
        Dado o cálculo do IRA, o menor número possível para a variável "semestre" é 1, e o maior é 6.
        """
        self.semester_range = {
            'min': 1,
            'max': 6,
        }

    def get_ira_value(self, disciplines) -> float:
        """
        Obter o valor do IRA a partir de um conjunto de menções.
        :param disciplines: A lista de disciplinas que um aluno pegou. Uma disciplina está no formato {'mencao': string, 'qtdCreditos': int, 'semestre': int}.

        :returns: Um float com o valor calculado do IRA.
        """
        valor_final = 0
        for discipline in disciplines:

            if not (self.semester_range['min'] <= discipline['semestre'] <= self.semester_range['max']):
                raise ValueError

            if discipline['mencao'] not in self.mencaoMap.keys():
                raise ValueError

            numerador = self.mencaoMap[discipline['mencao']] * \
                discipline['qtdCreditos'] * \
                discipline['semestre']

            denominador = discipline['qtdCreditos'] * discipline['semestre']
            valor_final += numerador/denominador

        return valor_final
            


