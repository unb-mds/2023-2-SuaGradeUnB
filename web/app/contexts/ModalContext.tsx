'use client';

import { createContext, useState } from 'react';

interface ModalContextType {
    activeModel: boolean;
    setActiveModal: React.Dispatch<React.SetStateAction<boolean>>;
}

export const ModalContext = createContext({} as ModalContextType);

export default function ModalContextProvider({ children }: {
    children: React.ReactNode;
}) {
    const [activeModel, setActiveModal] = useState(true);

    return (
        <ModalContext.Provider value={{ activeModel, setActiveModal }}>
            {children}
        </ModalContext.Provider>
    );
}