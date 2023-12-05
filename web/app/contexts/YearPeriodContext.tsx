'use client';

import { createContext, useEffect, useState } from 'react';
import retrieveYearAndPeriod, { YearPeriodType } from '../utils/api/retrieveYearAndPeriod';

interface YearPeriodContextType {
    periods: YearPeriodType,
    setPeriods: (value: YearPeriodType) => void,
}

interface YearPeriodContextProviderPropsType {
    children: React.ReactNode,
}

export const YearPeriodContext = createContext({} as YearPeriodContextType);

export default function YearPeriodContextProvider({ children }: YearPeriodContextProviderPropsType) {
    const [periods, setPeriods] = useState<YearPeriodType>({ 'year/period': [] });

    useEffect(() => {
        retrieveYearAndPeriod().then(data => setPeriods(data));
    }, []);

    return (
        <YearPeriodContext.Provider value={{ periods, setPeriods }}>
            {children}
        </YearPeriodContext.Provider>
    );
}