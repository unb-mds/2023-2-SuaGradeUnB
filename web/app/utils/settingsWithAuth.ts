import { settings } from '@/app/utils/settings';

export const settingsWithAuth = (access_token?: string) => {
    return {
        ...settings,
        headers: {
            ...settings.headers,
            'Authorization': `Bearer ${access_token}`
        }
    };
};