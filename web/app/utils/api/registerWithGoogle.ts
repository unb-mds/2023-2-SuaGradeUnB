import request from '../request';
import { AxiosResponse } from 'axios';
import { settings } from '../settings';

export default async function registerWithGoogle(access_token: string): Promise<AxiosResponse<any, any>> {
    const body = {
        access_token: access_token,
    };

    const response = await request.post('/users/register/google/', body, settings);

    return response;
}