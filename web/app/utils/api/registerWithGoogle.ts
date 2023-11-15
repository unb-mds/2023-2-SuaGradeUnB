import request from '../request';
import { AxiosResponse } from 'axios';

export default async function registerWithGoogle(access_token: string): Promise<AxiosResponse<any, any>> {
    const body = {
        access_token: access_token,
    };

    const settings = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        withCredentials: true,
    };

    const response = await request.post('/users/register/google/', body, settings);

    return response;
}