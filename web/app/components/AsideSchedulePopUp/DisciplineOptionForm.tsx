import { ChangeEvent, Dispatch, SetStateAction, useState } from 'react';
import useYearPeriod from '@/app/hooks/useYearPeriod';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';

import { errorToast } from '@/app/utils/errorToast';

import { DisciplineOptionFormPropsType, FormType, defaultFormData } from './types';
import { DisciplineType } from '@/app/utils/api/searchDiscipline';

import InputForm from './InputForm';

interface FormPropsType {
    form: FormType,
    disableDefault: boolean,
    setInfos: Dispatch<SetStateAction<Array<DisciplineType>>>,
    handleYearAndPeriodChange: (event: ChangeEvent<HTMLSelectElement>) => void,
}

function Form(props: FormPropsType) {
    const { formData, setFormData } = props.form;
    const { disableDefault, handleYearAndPeriodChange } = props;

    const { periods } = useYearPeriod();

    return (
        <>
            <div className='flex flex-col items-center gap-1 w-full max-w-md'>
                <span className='text-xl font-semibold'>Matéria</span>
                <InputForm form={{ formData, setFormData }} setInfos={props.setInfos} />
            </div>
            <div className='flex flex-col items-center gap-1 w-full max-w-md'>
                <span className='text-xl font-semibold'>Ano/Período</span>
                <select
                    className='bg-white shadow-md h-14 w-11/12 p-2 rounded-xl'
                    value={`${formData.year}/${formData.period}`}
                    onChange={event => handleYearAndPeriodChange(event)}
                >
                    <option disabled={disableDefault} value="">Selecione uma opção</option>
                    {periods['year/period'].map((item, index) => <option key={index} value={item}>{item}</option>)}
                </select>
            </div>
        </>
    );
}

function getYearAndPeriod(text: string) {
    const year = text.split('/')[0] || '';
    const period = text.split('/')[1] || '';

    return { year, period };
}

export default function DisciplineOptionForm(props: DisciplineOptionFormPropsType) {
    const { selectedClasses, currentYearPeriod, setCurrentYearPeriod } = useSelectedClasses();
    const [disableDefault, setDisableDefault] = useState(false);
    const [formData, setFormData] = useState(defaultFormData);

    function handleChangeYearAndPeriod(text: string, handleSetYearPeriod: () => void) {
        if (currentYearPeriod && currentYearPeriod != text && selectedClasses.size) {
            errorToast('Há disciplinas selecionadas de outro período, não pode haver mistura!');
        } else handleSetYearPeriod();
    }

    function handleYearAndPeriodChange(event: ChangeEvent<HTMLSelectElement>) {
        const text = event.target.value.trim();
        const { year, period } = getYearAndPeriod(text);

        if (year && period) {
            const handleSetYearPeriod = () => {
                setFormData({ ...formData, year: year, period: period });
                props.setInfos([]);
                setCurrentYearPeriod(text);
                setDisableDefault(true);
            };
            handleChangeYearAndPeriod(text, handleSetYearPeriod);
        }
    }

    return <Form form={{ formData, setFormData }} disableDefault={disableDefault}
        handleYearAndPeriodChange={handleYearAndPeriodChange} setInfos={props.setInfos} />;
}