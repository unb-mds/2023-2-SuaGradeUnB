'use client';

import { useContext } from 'react';
import { SelectedClassesContext } from '../contexts/SelectedClassesContext/SelectedClassesContext';

export default function useSelectedClasses() {
    const value = useContext(SelectedClassesContext);

    return value;
}