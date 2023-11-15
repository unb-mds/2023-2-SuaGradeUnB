'use client';

import { createContext, useState } from 'react';

interface User {
    is_anonymous: boolean;
    access?: string;
    first_name?: string;
    email?: string;
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

    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
}