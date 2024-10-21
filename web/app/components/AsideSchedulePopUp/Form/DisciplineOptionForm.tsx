import { Dispatch, SetStateAction, useEffect, useState } from 'react';
import useYearPeriod from '@/app/hooks/useYearPeriod';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';

import { errorToast } from '@/app/utils/toast';

import {
  DisciplineOptionFormPropsType,
  FormType,
  defaultFormData,
} from '../types/types';
import { DisciplineType } from '@/app/utils/api/searchDiscipline';

import InputForm from './InputForm';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../ui/select';

interface FormPropsType {
  form: FormType;
  setInfos: Dispatch<SetStateAction<Array<DisciplineType>>>;
  handleYearAndPeriodChange: (value: string) => void;
}

function Form(props: FormPropsType) {
  const { formData, setFormData } = props.form;
  const { handleYearAndPeriodChange } = props;

  const { periods } = useYearPeriod();

  return (
    <>
      <div className="flex flex-col items-center gap-1 w-full max-w-md">
        <span className="text-xl font-semibold">Ano/Período</span>

        <Select
          value={formData.year && formData.period ? `${formData.year}/${formData.period}` : undefined}
          onValueChange={(value) => {
            handleYearAndPeriodChange(value);
          }}
        >
          <SelectTrigger className="bg-white shadow-md h-14 w-11/12 p-2 rounded-xl">
            <SelectValue placeholder="Selecione uma opção" />
          </SelectTrigger>
          <SelectContent>
            {periods['year/period'].map((item, index) => (
              <SelectItem key={index} value={item}>
                {item}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="flex flex-col items-center gap-1 w-full max-w-md">
        <span className="text-xl font-semibold">Matéria</span>
        <InputForm form={{ formData, setFormData }} setInfos={props.setInfos} />
      </div>
    </>
  );
}

function getYearAndPeriod(text: string) {
  const year = text.split('/')[0] || defaultFormData.year;
  const period = text.split('/')[1] || defaultFormData.period;

  return { year, period };
}

function handleChangeYearAndPeriod(
  text: string,
  currentYearPeriod: string,
  selectedClasses: any,
  handleSetYearPeriod: () => void
) {
  if (currentYearPeriod && selectedClasses && currentYearPeriod != text) {
    errorToast(
      'Há disciplinas selecionadas de outro período, não pode haver mistura!'
    );
  } else handleSetYearPeriod();
}

export default function DisciplineOptionForm(
  props: DisciplineOptionFormPropsType
) {
  const { selectedClasses, currentYearPeriod, setCurrentYearPeriod } =
    useSelectedClasses();
  const [formData, setFormData] = useState(defaultFormData);

  useEffect(() => {
    if (formData == defaultFormData && selectedClasses.size) {
      const { year, period } = getYearAndPeriod(currentYearPeriod);
      setFormData({ ...formData, year: year, period: period });
    }
  }, [currentYearPeriod, formData, selectedClasses]);

  function handleYearAndPeriodChange(value: string) {
    const text = value.trim();
    const { year, period } = getYearAndPeriod(text);

    if (year && period) {
      const handleSetYearPeriod = () => {
        setFormData({ ...formData, year: year, period: period });
        props.setInfos([]);
        setCurrentYearPeriod(text);
      };
      handleChangeYearAndPeriod(
        text,
        currentYearPeriod,
        selectedClasses.size,
        handleSetYearPeriod
      );
    }
  }

  return (
    <Form
      form={{ formData, setFormData }}
      handleYearAndPeriodChange={handleYearAndPeriodChange}
      setInfos={props.setInfos}
    />
  );
}
