'use client';

import { createContext, useState } from 'react';

import { ClassType } from '../utils/api/searchDiscipline';
import { errorToast } from '../utils/errorToast';

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
    currentYearPeriod: string,
    setCurrentYearPeriod: (string: string) => void
}

interface SelectedClassesContextProviderPropsType {
    children: React.ReactNode
}

export const SelectedClassesContext = createContext({} as SelectedClassesContextType);

export default function SelectedClassesContextProvider({ children, ...props }: SelectedClassesContextProviderPropsType) {
    const [selectedClasses, setSelectedClassesDefault] = useState<SelectedClassesType>(new Map());
    const [classesChange, setClassesChange] = useState(false);
    const [currentYearPeriod, setCurrentYearPeriod] = useState('');

    const setSelectedClasses = (value: SelectedClassesType) => {
        let hasError = false;
        const handleError = (message: string) => {
            errorToast(message);
            hasError = true;
        };

        const MAX_CLASSES = 4;
        const MAX_DISCIPLINES = 11;

        value.forEach((classes, disciplineId) => {
            if (classes.size > MAX_CLASSES) handleError(`Você só pode escolher até ${MAX_CLASSES} aulas da mesma disciplina!`);
        });

        if (value.size > MAX_DISCIPLINES) handleError(`Você só pode escolher até ${MAX_DISCIPLINES} disciplinas!`);

        if (!hasError) {
            if (!value.size) setCurrentYearPeriod('');
            setSelectedClassesDefault(value);
            setClassesChange(!classesChange);
        }
    };

    return (
        <SelectedClassesContext.Provider value={{ classesChange, selectedClasses, setSelectedClasses, currentYearPeriod, setCurrentYearPeriod }}>
            {children}
        </SelectedClassesContext.Provider>
    );
}