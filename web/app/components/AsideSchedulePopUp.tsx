import { Dispatch, LegacyRef, SetStateAction, useState } from 'react';

import Button from './Button';
import searchDiscipline, { ResponseType } from '../utils/api/searchDiscipline';
import toast from 'react-hot-toast';

interface AsideSchedulePopUpPropsType {
    content: {
        showContent: boolean,
        setShowContent: Dispatch<SetStateAction<boolean>>
    }
    divAddClassRef?: LegacyRef<HTMLDivElement> | undefined
}

const defaultFormData = {
    search: '',
    year: '',
    period: ''
};

export default function AsideSchedulePopUp(props: AsideSchedulePopUpPropsType) {
    const [disableDefault, setDisableDefault] = useState(false);
    const [formData, setFormData] = useState(defaultFormData);
    const [searchedDisciplineInfos, setSearchedDisciplineInfos] = useState([] as ResponseType);

    const { showContent, setShowContent } = props.content;

    return (
        <div className='flex justify-center'>
            <div
                ref={props.divAddClassRef}
                className={`flex flex-col justify-between items-center w-11/12 ${showContent ? 'py-5 h-5/6' : 'h-0'} transition-all duration-500 absolute bottom-0 rounded-t-[40px] bg-snow-secondary z-10`}
            >
                {showContent && (
                    <>
                        <section className='flex flex-col items-center gap-5 w-full h-[90%] text-[#333333]'>
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
                                        onClick={async () => {
                                            const { search, year, period } = formData;

                                            const textSearch = search.trim();

                                            if (!textSearch) toast.error('Escreva no nome da disciplina');
                                            else if (!year || !period) toast.error('Escolha o ano/período');
                                            else {
                                                const data = await searchDiscipline(textSearch, year, period);
                                                if (data) setSearchedDisciplineInfos(data);
                                            }
                                        }}
                                        className='material-symbols-rounded'
                                    >
                                        search
                                    </button>
                                </div>
                            </div>
                            <div className='flex flex-col items-center gap-1'>
                                <span className='text-xl font-semibold'>Ano/Período</span>
                                <select
                                    className='bg-white h-14 w-80 p-2 rounded-xl'
                                    value={`${formData.year}/${formData.period}`}
                                    onChange={(e) => {
                                        const text = e.target.value.trim();

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
                                    }}
                                >
                                    <option disabled={disableDefault} value="">Selecione uma opção</option>
                                    <option value="2023/2">2023/2</option>
                                    <option value="2024/1">2024/1</option>
                                </select>
                            </div>
                            <div className='flex flex-col gap-5 overflow-auto max-h-full w-10/12 mx-5'>
                                {searchedDisciplineInfos.map((discipline) => (
                                    <div className='flex flex-col gap-5' key={discipline.code}>
                                        <span className='font-semibold'>{discipline.name} - {discipline.code}</span>
                                        {discipline.classes.map((cls, index) => (
                                            <div className='flex flex-col' key={index}>
                                                <div>
                                                    <span className='font-semibold'>Sala:</span> {cls.classroom}
                                                </div>
                                                <div className='flex gap-2'>
                                                    <span className='font-semibold'>Horários:</span> {cls.schedule}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                ))}
                            </div>
                        </section>
                        <Button onClick={() => setShowContent(false)} className='bg-primary w-52'>
                            Adicionar
                        </Button>
                    </>
                )}
            </div>
        </div >
    );
}