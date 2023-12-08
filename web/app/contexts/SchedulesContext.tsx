'use client';

import { createContext, useEffect, useState } from 'react';

import { ClassType } from '../utils/api/searchDiscipline';

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
    setLocalSchedules: (newSchedules: Array<ScheduleClassType> | Array<Array<ScheduleClassType>>, add?: boolean) => void;
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
        const localSchedulesFromJSON: SchedulesType = localJSON;
        setLocalDefaultSchedules(localSchedulesFromJSON);
    }, []);

    const setLocalSchedules = (newSchedules: Array<ScheduleClassType> | Array<Array<ScheduleClassType>>, add: boolean = true) => {
        if (add) {
            const newLocalSchedules = [
                ...newSchedules,
                ...localSchedules,
            ];
            const uniqueSchedules = newLocalSchedules.filter((schedule, index, self) => {
                const stringSchedule = JSON.stringify(schedule);
                return index === self.findIndex((s) => JSON.stringify(s) === stringSchedule);
            });
            localStorage.setItem('schedules', JSON.stringify(uniqueSchedules));
        } else localStorage.setItem('schedules', JSON.stringify(newSchedules));

        const localJSON = JSON.parse(localStorage.getItem('schedules') || '[]');
        const localSchedulesFromJSON: SchedulesType = localJSON;
        setLocalDefaultSchedules(localSchedulesFromJSON);
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