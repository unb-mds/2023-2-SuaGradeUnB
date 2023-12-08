'use client';

import { createContext, useState } from 'react';

interface ModalContextType {
    activeModel: boolean;
    setActiveModel: React.Dispatch<React.SetStateAction<boolean>>;
}

export const ModalContext = createContext({} as ModalContextType);

export default function ModalContextProvider({ children }: {
    children: React.ReactNode;
}) {
    const [activeModel, setActiveModel] = useState(true);

    return (
        <ModalContext.Provider value={{ activeModel, setActiveModel }}>
            {children}
        </ModalContext.Provider>
    );
}