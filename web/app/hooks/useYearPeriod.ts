'use client';

import { useContext } from 'react';
import { YearPeriodContext } from '../contexts/YearPeriodContext';

export default function useYearPeriod() {
    const value = useContext(YearPeriodContext);

    return value;
}