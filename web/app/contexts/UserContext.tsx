'use client';

import { createContext, useEffect, useState } from 'react';

import { UserData } from '../components/SignInSection';

import { settings } from '../utils/settings';
import request from '../utils/request';
import getSchedules from '../utils/api/getSchedules';
import { errorToast } from '../utils/errorToast';
import useSchedules from '../hooks/useSchedules';

export interface User {
    is_anonymous: boolean;
    access?: string;
    first_name?: string;
    email?: string;
    picture_url?: string;
}

export const defaultUser: User = {
    is_anonymous: true,
};

export interface UserContextType {
    user: User;
    setUser: React.Dispatch<React.SetStateAction<User>>;
    isLoading: boolean;
    setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

interface UserContextProviderProps {
    children: React.ReactNode;
}

export const UserContext = createContext({} as UserContextType);

export default function UserContextProvider({ children, ...props }: UserContextProviderProps) {
    const [user, setUser] = useState<User>(defaultUser);
    const [isLoading, setLoading] = useState(true);

    const { cloudSchedules, setCloudSchedules } = useSchedules();

    useEffect(() => {
        request.post('/users/login/', {}, settings).then(response => {
            const userData: UserData = response.data;
            setUser({
                is_anonymous: false,
                access: userData.access,
                first_name: userData.first_name,
                email: userData.email,
                picture_url: userData.picture_url
            });
            setLoading(false);
        }).catch(error => {
            setUser(defaultUser);
            setLoading(false);
        });
    }, [setUser]);

    useEffect(() => {
        if (!user.is_anonymous && !cloudSchedules.length) {
            getSchedules(user.access).then(response => {
                if (response.status == 200 && response.data.length) {
                    setCloudSchedules(response.data);
                }
            }).catch(error => {
                errorToast('Não foi possível carregar suas grades na nuvem.');
            });
        }
    }, [user, cloudSchedules, setCloudSchedules]);

    return (
        <UserContext.Provider value={{ user, setUser, isLoading, setLoading }}>
            {children}
        </UserContext.Provider>
    );
}