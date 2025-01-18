import { render, screen, fireEvent } from '@testing-library/react';
import DisciplineOptionForm from './DisciplineOptionForm';
import { useSelectedClasses } from '../../hooks'; 
import { errorToast } from '../../utils/toasts';  

jest.mock('../../hooks'); 
jest.mock('../../utils/toasts'); 

describe('handleChangeYearAndPeriod', () => {
  
  const mockSetYearPeriod = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();  
  });

  test('deve disparar um erro quando há disciplinas de períodos diferentes', () => {
  
    useSelectedClasses.mockReturnValue({
      selectedClasses: new Set(['Disciplina 1']),
      currentYearPeriod: '2023-1',
      setCurrentYearPeriod: mockSetYearPeriod,
    });

   
    const text = '2023-2';  
    const currentYearPeriod = '2023-1';
    const selectedClasses = new Set(['Disciplina 1']);
    
    handleChangeYearAndPeriod(text, currentYearPeriod, selectedClasses, mockSetYearPeriod);

    expect(errorToast).toHaveBeenCalledWith('Há disciplinas selecionadas de outro período, não pode haver mistura!');
  });

  test('deve atualizar o estado para o novo período quando não houver conflito de períodos', () => {
    useSelectedClasses.mockReturnValue({
      selectedClasses: new Set(),
      currentYearPeriod: '2023-1',
      setCurrentYearPeriod: mockSetYearPeriod,
    });
    const text = '2023-1'; 
    const currentYearPeriod = '2023-1';
    const selectedClasses = new Set();

    handleChangeYearAndPeriod(text, currentYearPeriod, selectedClasses, mockSetYearPeriod);

    expect(mockSetYearPeriod).toHaveBeenCalledTimes(1);
  });
});
