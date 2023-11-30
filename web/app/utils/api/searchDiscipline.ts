import toast from 'react-hot-toast';

import request from '../request';
import { settings } from '../settings';

export type ClassType = {
    id: number,
    _class: string,
    classroom: string,
    days: Array<string>,
    schedule: string,
    special_dates: Array<Array<string>>,
    teachers: Array<string>
}

export type DisciplineType = {
    expanded: boolean,
    id: number,
    code: string,
    name: string,
    classes: Array<ClassType>
}

export default async function searchDiscipline(search: string, year: string, period: string) {
    const params = {
        search: search,
        year: year,
        period: period
    };

    try {
        const response = await request.get('/courses/', {
            ...settings,
            params: params
        });

        const data: Array<DisciplineType> = response.data;
        return data;
    } catch (error: any) {
        const mensagem = error.response.data.errors;
        if(mensagem === 'search must have at least 4 characters'){
            toast.error('A busca deve conter pelo menos 4 caracteres');
        }
    }
} 