'use client';

import { createContext, useState } from 'react';

import { ClassValueType } from './SelectedClassesContext';

interface ClassesToShowContextType {
    classesToShow: Array<ClassValueType>,
    setClassesToShow: (value: Array<ClassValueType>) => void;
}

interface ClassesToShowContextProviderPropsType {
    children: React.ReactNode
}

export const ClassesToShowContext = createContext({} as ClassesToShowContextType);

export default function ClassesToShowContextProvider({ children, ...props }: ClassesToShowContextProviderPropsType) {
    const [classesToShow, setClassesToShow] = useState<Array<ClassValueType>>([]);

    return (
        <ClassesToShowContext.Provider value={{ classesToShow, setClassesToShow }}>
            {children}
        </ClassesToShowContext.Provider>
    );
}