import { Dispatch, LegacyRef, SetStateAction, useState } from 'react';

import Button from './Button';

import searchDiscipline, { ResponseType } from '../utils/api/searchDiscipline';

import toast from 'react-hot-toast';

import styles from '@/app/components/styles/tooltip.module.css';

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
                                                if (data) {
                                                    let infos: ResponseType[0][] = [];
                                                    data.forEach(discipline => {
                                                        infos.push({
                                                            ...discipline,
                                                            expanded: false
                                                        });
                                                    });
                                                    setSearchedDisciplineInfos(infos);
                                                }
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
                                    className='bg-white shadow-md h-14 w-80 p-2 rounded-xl'
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
                            <div className='flex flex-col gap-2 w-10/12 h-[50%] overflow-auto text-lg'>
                                {searchedDisciplineInfos.map((discipline, index) => (
                                    <>
                                        <button
                                            onClick={() => {
                                                let newInfo: ResponseType[0][] = [];
                                                searchedDisciplineInfos.forEach((discipline, number) => {
                                                    if (number != index) newInfo.push(discipline);
                                                    else {
                                                        newInfo.push({
                                                            ...discipline,
                                                            expanded: !discipline.expanded
                                                        });
                                                    }
                                                });

                                                setSearchedDisciplineInfos(newInfo);
                                            }}
                                            className='flex items-center gap-3'
                                        >
                                            <span className="material-symbols-rounded">
                                                {discipline.expanded ? 'expand_less' : 'expand_more'}
                                            </span>
                                            <span className='font-semibold'>{discipline.name} - {discipline.code}</span>
                                        </button>
                                        {discipline.expanded &&
                                            <div className='overflow-auto min-h-full'>
                                                {discipline.classes.map((cls, index) => (
                                                    <div className='flex flex-col hover:bg-gray-300 hover:bg-opacity-40 rounded-md p-2' key={index}>
                                                        <div>
                                                            <span className='font-semibold'>Sala:</span> {cls.classroom}
                                                        </div>
                                                        <div className='flex gap-1'>
                                                            <span className='font-semibold'>Horários:</span> {cls.schedule}
                                                            <div className={styles.tooltip}>
                                                                <span className='material-symbols-rounded text-xs'>question_mark</span>
                                                                <span className={`${styles.tooltiptext} p-2`}>
                                                                    {cls.days.map((day, index) =>
                                                                        <div key={index}>
                                                                            {day}
                                                                        </div>
                                                                    )}
                                                                </span>
                                                            </div>
                                                        </div>
                                                        <div>
                                                            <span className='font-semibold'>Professor:</span> {cls.teachers[0]} {cls.teachers.length > 1 && 'e outros'}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        }
                                    </>
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