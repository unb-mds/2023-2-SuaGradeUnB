'use client';

import { createContext, useState } from 'react';

import { errorToast } from '../../utils/toast';

import { ProviderJSXPropsType, SelectedClassesContextProviderPropsType, SelectedClassesContextType, SelectedClassesType } from './types';


let hasError = false;
const MAX_CLASSES = 4;
const MAX_DISCIPLINES = 11;

export const SelectedClassesContext = createContext({} as SelectedClassesContextType);

const handleError = (message: string) => {
    errorToast(message);
    hasError = true;
};

function handleMaxDisciplinesError(value: SelectedClassesType) {
    if (value.size > MAX_DISCIPLINES) {
        handleError(`Você só pode escolher até ${MAX_DISCIPLINES} disciplinas!`);
    }
}

function handleMaxClassesError(value: SelectedClassesType) {
    value.forEach(classes => {
        if (classes.size > MAX_CLASSES) {
            handleError(`Você só pode escolher até ${MAX_CLASSES} aulas da mesma disciplina!`);
        }
    });
}

function ProviderJSX({ children, ...props }: ProviderJSXPropsType) {
    return (
        <SelectedClassesContext.Provider value={props}>
            {children}
        </SelectedClassesContext.Provider>
    );
}

export default function SelectedClassesContextProvider({ children }: SelectedClassesContextProviderPropsType) {
    const [selectedClasses, setSelectedClassesDefault] = useState<SelectedClassesType>(new Map());
    const [classesChange, setClassesChange] = useState(false);
    const [currentYearPeriod, setCurrentYearPeriod] = useState('');

    function handleNoError(value: SelectedClassesType) {
        if (!value.size) setCurrentYearPeriod('');
        setSelectedClassesDefault(value);
        setClassesChange(!classesChange);
    }

    const setSelectedClasses = (value: SelectedClassesType) => {
        hasError = false;

        handleMaxClassesError(value);
        handleMaxDisciplinesError(value);
        if (!hasError) handleNoError(value);
    };

    return ProviderJSX({ children, selectedClasses, setSelectedClasses, classesChange, currentYearPeriod, setCurrentYearPeriod });
}