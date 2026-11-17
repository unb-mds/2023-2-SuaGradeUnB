'use client';

import { createContext, useEffect, useRef, useState } from 'react';
import useYearPeriod from '../../hooks/useYearPeriod';

import { errorToast } from '../../utils/toast';

import { ProviderJSXPropsType, SelectedClassesContextProviderPropsType, SelectedClassesContextType, SelectedClassesType } from './types';
import { clearDraft, MAX_CLASSES, MAX_DISCIPLINES, readDraft, restoreDraft, saveDraft, Selection } from './draft';


let hasError = false;

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
    const [selection, setSelection] = useState<Selection>({ selectedClasses: new Map(), currentYearPeriod: '' });
    const selectionRef = useRef(selection);
    const interacted = useRef(false);
    const [classesChange, setClassesChange] = useState(false);
    const { periods } = useYearPeriod();
    const { selectedClasses, currentYearPeriod } = selection;

    useEffect(() => {
        // Wait until the offered periods arrive; the initial empty state must never be saved.
        if (!periods['year/period'].length || interacted.current) return;
        const draft = readDraft();
        if (!draft) return;
        if (!periods['year/period'].includes(draft.yearPeriod)) {
            clearDraft();
            return;
        }
        let active = true;
        restoreDraft(draft).then(restored => {
            if (!active || interacted.current) return;
            selectionRef.current = restored;
            setSelection(restored);
            setClassesChange(value => !value);
            saveDraft(restored);
        }).catch(() => {
            if (active && !interacted.current) {
                errorToast('Não foi possível recuperar a seleção. Recarregue para tentar novamente.');
            }
            // Keep the draft on network failure so another reload can retry.
        });
        return () => { active = false; };
    }, [periods]);

    function updateSelection(value: Selection) {
        // A user action wins over a pending restore, including clearing the selection.
        interacted.current = true;
        selectionRef.current = value;
        setSelection(value);
        setClassesChange(previous => !previous);
        saveDraft(value);
    }

    function handleNoError(value: SelectedClassesType) {
        updateSelection({ selectedClasses: value, currentYearPeriod: value.size ? selectionRef.current.currentYearPeriod : '' });
    }

    const setCurrentYearPeriod = (value: string) => {
        const current = selectionRef.current;
        updateSelection({
            currentYearPeriod: value,
            selectedClasses: value === current.currentYearPeriod ? current.selectedClasses : new Map()
        });
    };

    const setSelectedClasses = (value: SelectedClassesType) => {
        hasError = false;

        handleMaxClassesError(value);
        handleMaxDisciplinesError(value);
        if (!hasError) handleNoError(value);
    };

    return ProviderJSX({ children, selectedClasses, setSelectedClasses, classesChange, currentYearPeriod, setCurrentYearPeriod });
}
