import toast from 'react-hot-toast';

import request from '../request';
import { settings } from '../settings';

export type ResponseType = Array<{
    expanded: boolean,
    code: string,
    name: string,
    classes: Array<{
        _class: string,
        classroom: string,
        days: Array<string>,
        schedule: string,
        teachers: Array<string>
    }>
}>

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

        const data: ResponseType = response.data;
        return data;
    } catch (error: any) {
        toast.error(error.response.data.detail);
    }
} 