import { UserContextType, defaultUser } from '@/app/contexts/UserContext';

import request from '../request';
import { settings } from '../settings';

import { AppRouterInstance } from 'next/dist/shared/lib/app-router-context.shared-runtime';

import toast from 'react-hot-toast';

interface handleLogoutParamsType {
    userContext: UserContextType,
    router: AppRouterInstance
};

export default function handleLogout({
    userContext,
    router
}: handleLogoutParamsType) {
    const { user, setUser } = userContext;

    if (!user.is_anonymous) {
        request.post('/users/logout/', {}, settings).then(response => {
            if (response.status == 200) {
                setUser(defaultUser);
                router.replace('/');
            }
        }).catch(error => toast.error('Não foi possível sair!'));
    }
    else router.replace('/');
}