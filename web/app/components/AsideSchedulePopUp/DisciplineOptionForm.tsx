import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import searchDiscipline, { DisciplineType } from '@/app/utils/api/searchDiscipline';
import { errorToast } from '@/app/utils/errorToast';

import { ChangeEvent, Dispatch, SetStateAction, useEffect, useRef, useState } from 'react';

import toast from 'react-hot-toast';

interface DisciplineOptionFormPropsType {
    setInfos: Dispatch<SetStateAction<Array<DisciplineType>>>
}

const defaultFormData = {
    search: '',
    year: '',
    period: ''
};

export default function DisciplineOptionForm(props: DisciplineOptionFormPropsType) {
    const { selectedClasses, currentYearPeriod, setCurrentYearPeriod } = useSelectedClasses();
    const [disableDefault, setDisableDefault] = useState(false);
    const [formData, setFormData] = useState(defaultFormData);

    const inputRef = useRef<HTMLInputElement>(null);

    function handleYearAndPeriodChange(event: ChangeEvent<HTMLSelectElement>) {
        const text = event.target.value.trim();

        const year = text.split('/')[0] || '';
        const period = text.split('/')[1] || '';

        if (year && period) {
            const handleSetYearPeriod = () => {
                setFormData({
                    ...formData,
                    year: year,
                    period: period
                });
                props.setInfos([]);
                setCurrentYearPeriod(text);
                setDisableDefault(true);
            };

            if (currentYearPeriod) {
                if (currentYearPeriod != text && selectedClasses.size) {
                    errorToast('Há disciplinas selecionadas de outro período, não pode haver mistura!');
                } else handleSetYearPeriod();
            } else handleSetYearPeriod();
        }
    }

    async function handleSearch(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();

        if (inputRef && inputRef.current) {
            inputRef.current.blur();
        }

        const { search, year, period } = formData;

        const textSearch = search.trim();

        if (!textSearch) toast.error('Escreva no nome da disciplina');
        else if (!year || !period) toast.error('Escolha o ano/período');
        else {
            const data = await searchDiscipline(textSearch, year, period);
            if (data) {
                let infos: Array<DisciplineType> = [];
                data.forEach(discipline => {
                    infos.push({
                        ...discipline,
                        expanded: false
                    });
                });
                props.setInfos(infos);
            }
        }
    }

    return (
        <>
            <div className='flex flex-col items-center gap-1'>
                <span className='text-xl font-semibold'>Matéria</span>
                <form
                    className='flex items-center w-80 px-2 bg-white shadow-md rounded-xl'
                    onSubmit={handleSearch}
                >
                    <input
                        type="text"
                        placeholder='Nome da matéria...'
                        value={formData.search}
                        onChange={(e) => setFormData({
                            ...formData,
                            search: e.target.value
                        })}
                        ref={inputRef}
                        className='h-14 p-2 w-11/12 rounded-xl focus:outline-none'
                    />
                    <button
                        className='material-symbols-rounded'
                        type='submit'
                    >
                        search
                    </button>
                </form>
            </div>
            <div className='flex flex-col items-center gap-1'>
                <span className='text-xl font-semibold'>Ano/Período</span>
                <select
                    className='bg-white shadow-md h-14 w-80 p-2 rounded-xl'
                    value={`${formData.year}/${formData.period}`}
                    onChange={event => handleYearAndPeriodChange(event)}
                >
                    <option disabled={disableDefault} value="">Selecione uma opção</option>
                    <option value="2023/2">2023/2</option>
                    <option value="2024/1">2024/1</option>
                </select>
            </div>
        </>
    );
}