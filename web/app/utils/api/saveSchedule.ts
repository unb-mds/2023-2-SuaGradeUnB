import { ScheduleClassType } from '@/app/contexts/SchedulesContext';

import request from '../request';
import { settingsWithAuth } from '../settingsWithAuth';

export default async function saveSchedule(schedule?: Array<ScheduleClassType>, access_token?: string) {
    const response = await request.post('/courses/schedules/', schedule, settingsWithAuth(access_token));

    return response;
}