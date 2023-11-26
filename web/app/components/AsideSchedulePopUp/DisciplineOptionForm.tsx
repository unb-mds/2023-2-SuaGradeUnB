import searchDiscipline, { DisciplineType } from '@/app/utils/api/searchDiscipline';

import { ChangeEvent, Dispatch, SetStateAction, useState } from 'react';

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
    const [disableDefault, setDisableDefault] = useState(false);
    const [formData, setFormData] = useState(defaultFormData);

    function handleYearAndPeriodChange(event: ChangeEvent<HTMLSelectElement>) {
        const text = event.target.value.trim();

        const year = text.split('/')[0] || '';
        const period = text.split('/')[1] || '';

        if (year && period) {
            setFormData({
                ...formData,
                year: year,
                period: period
            });
            setDisableDefault(true);
        }
    }

    async function handleSearch() {
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
                <div className='flex items-center w-80 px-2 bg-white shadow-md rounded-xl'>
                    <input
                        type="text"
                        placeholder='Nome da matéria...'
                        value={formData.search}
                        onChange={(e) => setFormData({
                            ...formData,
                            search: e.target.value
                        })}
                        className='h-14 p-2 w-11/12 rounded-xl focus:outline-none'
                    />
                    <button
                        onClick={handleSearch}
                        className='material-symbols-rounded'
                    >
                        search
                    </button>
                </div>
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