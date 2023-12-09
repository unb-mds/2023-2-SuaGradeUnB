import request from '../request';
import { settingsWithAuth } from '../settingsWithAuth';

export default async function deleteSchedule(scheduleId?: number, access_token?: string) {
    const response = await request.delete(
        `/courses/schedules/${scheduleId}/`,
        settingsWithAuth(access_token)
    );

    return response;
}