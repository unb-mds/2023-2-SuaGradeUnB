'use client';

import React, { createContext, useEffect, useState } from 'react';

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

export interface CloudScheduleType {
    id: number;
    created_at: string;
    classes: Array<ScheduleClassType>;
};

type SchedulesType = Array<Array<ScheduleClassType>>;
type SchedulesCloudType = Array<CloudScheduleType>;

interface SchedulesContextType {
    localSchedules: SchedulesType;
    setLocalSchedules: (newSchedules: Array<ScheduleClassType> | Array<Array<ScheduleClassType>>, add?: boolean) => void;
    cloudSchedules: SchedulesCloudType;
    setCloudSchedules: (newSchedules: SchedulesCloudType) => void;
}

export const SchedulesContext = createContext<SchedulesContextType>({} as SchedulesContextType);

export default function SchedulesContextProvider({ children }: {
    children: React.ReactNode;
}) {
    const [localSchedules, setLocalDefaultSchedules] = useState<SchedulesType>([] as SchedulesType);
    const [cloudSchedules, setCloudDefaultSchedules] = useState<SchedulesCloudType>([] as SchedulesCloudType);

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

    const setCloudSchedules = (newSchedules: SchedulesCloudType) => {
        const data: Array<any> = newSchedules;
        data.forEach((schedule, index) => {
            data[index].classes = JSON.parse(schedule.classes);
        });
        setCloudDefaultSchedules(data);
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