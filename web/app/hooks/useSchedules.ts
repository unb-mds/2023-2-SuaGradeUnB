'use client';

import { useContext } from 'react';
import { SchedulesContext } from '../contexts/SchedulesContext';

export default function useSchedules() {
    const value = useContext(SchedulesContext);

    return value;
}