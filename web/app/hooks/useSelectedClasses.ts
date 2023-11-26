'use client';

import { useContext } from 'react';
import { SelectedClassesContext } from '../contexts/SelectedClassesContext';

export default function useSelectedClasses() {
    const value = useContext(SelectedClassesContext);

    return value;
}