import toast from 'react-hot-toast';

import request from '../request';
import { settings } from '../settings';

export interface YearPeriodType {
    'year/period': Array<string>;
}

export default async function retrieveYearAndPeriod() {
    try {
        const response = await request.get('/courses/year-period/', settings);

        const data: YearPeriodType = response.data;
        return data;
    } catch (error: any) {
        toast.error(error.response.data.detail);
        return { 'year/period': [] };
    }
}