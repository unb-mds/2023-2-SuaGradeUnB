'use client';

import { createContext, useEffect, useState } from 'react';
import request from '../utils/request';
import { UserData } from '../components/SignInSection';
import { settings } from '../utils/settings';

interface User {
    is_anonymous: boolean;
    access?: string;
    first_name?: string;
    email?: string;
    picture_url?: string;
}

export const defaultUser: User = {
    is_anonymous: true,
};

interface UserContextType {
    user: User;
    setUser: React.Dispatch<React.SetStateAction<User>>;
}

interface UserContextProviderProps {
    children: React.ReactNode;
}

export const UserContext = createContext({} as UserContextType);

export default function UserContextProvider({ children, ...props }: UserContextProviderProps) {
    const [user, setUser] = useState<User>(defaultUser);

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
        }).catch(error => {
            setUser(defaultUser);
        });
    }, [setUser]);

    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
}