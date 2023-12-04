import { useRef } from 'react';

import toast from 'react-hot-toast';

import searchDiscipline, { DisciplineType } from '@/app/utils/api/searchDiscipline';

import { FormData, FormType, InputFormPropsType } from './types';

interface FormPropsType {
    form: FormType,
    handleSearch: (event: React.FormEvent<HTMLFormElement>) => Promise<void>,
    inputRef: React.RefObject<HTMLInputElement>
}

function Form(props: FormPropsType) {
    const { formData, setFormData } = props.form;
    const { handleSearch, inputRef } = props;

    return (
        <form className='flex items-center w-11/12 px-2 bg-white shadow-md rounded-xl' onSubmit={handleSearch}>
            <input
                type="text"
                placeholder='Nome da matéria...'
                value={formData.search}
                onChange={(e) => setFormData({ ...formData, search: e.target.value })}
                ref={inputRef}
                className='h-14 p-2 w-full rounded-xl focus:outline-none'
            />
            <button className='material-symbols-rounded' type='submit' >search</button>
        </form>
    );
}

async function makeDisciplineSearch(textSearch: string, year: string, period: string, setInfos: (infos: Array<DisciplineType>) => void) {
    const data = await searchDiscipline(textSearch, year, period);
    if (data) {
        let infos: Array<DisciplineType> = [];
        data.forEach(discipline => infos.push({ ...discipline, expanded: false }));
        setInfos(infos);
    }
}

async function handleDisciplineSearch(formData: FormData, setInfos: (infos: Array<DisciplineType>) => void) {
    const { search, year, period } = formData;
    const textSearch = search.trim();

    if (!textSearch) toast.error('Escreva no nome da disciplina');
    else if (!year || !period) toast.error('Escolha o ano/período');
    else await makeDisciplineSearch(textSearch, year, period, setInfos);
}

export default function InputForm(props: InputFormPropsType) {
    const inputRef = useRef<HTMLInputElement>(null);
    const { formData } = props.form;

    async function handleSearch(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();

        if (inputRef && inputRef.current) inputRef.current.blur();

        await handleDisciplineSearch(formData, props.setInfos);
    }

    return <Form form={props.form} handleSearch={handleSearch} inputRef={inputRef} />;
}