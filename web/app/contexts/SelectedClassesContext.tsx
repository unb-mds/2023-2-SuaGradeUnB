'use client';

import { createContext, useState } from 'react';

import { ClassType } from '../utils/api/searchDiscipline';

export type ClassValueType = {
    class: ClassType,
    discipline: {
        id: number,
        name: string,
        code: string
    }
}
export type SelectedClassesType = Map<number, Map<number, ClassValueType>>;

interface SelectedClassesContextType {
    classesChange: boolean,
    selectedClasses: SelectedClassesType,
    setSelectedClasses: (value: SelectedClassesType) => void;
}

interface SelectedClassesContextProviderPropsType {
    children: React.ReactNode
}

export const SelectedClassesContext = createContext({} as SelectedClassesContextType);

export default function SelectedClassesContextProvider({ children, ...props }: SelectedClassesContextProviderPropsType) {
    const [selectedClasses, setSelectedClassesDefault] = useState<SelectedClassesType>(new Map());
    const [classesChange, setClassesChange] = useState(false);

    const setSelectedClasses = (value: SelectedClassesType) => {
        setSelectedClassesDefault(value);
        setClassesChange(!classesChange);
    };

    return (
        <SelectedClassesContext.Provider value={{ classesChange, selectedClasses, setSelectedClasses }}>
            {children}
        </SelectedClassesContext.Provider>
    );
}