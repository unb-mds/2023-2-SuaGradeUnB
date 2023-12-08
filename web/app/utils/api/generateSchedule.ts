import { AxiosResponse } from 'axios';

import request from '../request';
import { settings } from '../settings';

type EachFieldNumber = 1 | 2 | 3;
type PreferenceType = [EachFieldNumber, EachFieldNumber, EachFieldNumber];

//Promise<AxiosResponse<any, any>>
export default async function generateSchedule(classes_id: Array<number>, preference?: PreferenceType) {
    const body: {
        classes: Array<number>,
        preference?: PreferenceType,
    } = {
        classes: classes_id,
    };
    if (preference) body.preference = preference;

    const response = await request.post('/courses/schedule/', body, settings);

    return response;
}