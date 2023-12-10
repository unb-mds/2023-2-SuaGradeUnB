import request from '../request';
import { settingsWithAuth } from '../settingsWithAuth';

export default async function getSchedules(access_token?: string) {
    const response = request.get('/courses/schedules/', settingsWithAuth(access_token));

    return response;
}