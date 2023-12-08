'use client';

import { createContext, useEffect, useState } from 'react';

import { ClassType } from '../utils/api/searchDiscipline';
import { set } from 'lodash';

export interface ScheduleClassType extends ClassType {
    discipline: {
        id: number;
        name: string;
        code: string;
        department: number;
        unicode_name: string;
    }
};

type SchedulesType = Array<Array<ScheduleClassType>>;

interface SchedulesContextType {
    localSchedules: SchedulesType;
    setLocalSchedules: (newSchedules: Array<ScheduleClassType>) => void;
    cloudSchedules: SchedulesType;
    setCloudSchedules: React.Dispatch<React.SetStateAction<SchedulesType>>;
}

export const SchedulesContext = createContext<SchedulesContextType>({} as SchedulesContextType);

export default function SchedulesContextProvider({ children }: {
    children: React.ReactNode;
}) {
    const [localSchedules, setLocalDefaultSchedules] = useState<SchedulesType>([] as SchedulesType);
    const [cloudSchedules, setCloudSchedules] = useState<SchedulesType>([] as SchedulesType);

    useEffect(() => {
        const localJSON = JSON.parse(localStorage.getItem('schedules') || '[]');
        const localSchedules: SchedulesType = localJSON;
        setLocalDefaultSchedules(localSchedules);
    }, []);

    const setLocalSchedules = (newSchedules: Array<ScheduleClassType>) => {
        setLocalDefaultSchedules([
            ...localSchedules,
            newSchedules,
        ]);
        localStorage.setItem('schedules', JSON.stringify([
            ...localSchedules,
            ...newSchedules,
        ]));
    };

    return (
        <SchedulesContext.Provider value={{
            localSchedules, setLocalSchedules,
            cloudSchedules, setCloudSchedules
        }}>
            {children}
        </SchedulesContext.Provider>
    );
}