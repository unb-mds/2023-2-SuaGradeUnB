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

    def get_ira_value(self, mencoes):
        """
        Obter o valor do IRA a partir de um conjunto de menções.

        :param mencoes: A lista de menções. Uma menção está no formato {'mencao': string, 'qtdCreditos': int, 'semestre': int}.
        """
        valor_final = 0
        for mencao in mencoes:

            if not (1 <= mencao['semestre'] <= 6):
                raise ValueError

            if mencao['mencao'] not in self.mencaoMap.keys():
                raise ValueError

            numerador = self.mencaoMap[mencao['mencao']] * \
                mencao['qtdCreditos'] * \
                mencao['semestre']

            denominador = mencao['qtdCreditos'] * mencao['semestre']
            valor_final += numerador/denominador

        return valor_final
            


