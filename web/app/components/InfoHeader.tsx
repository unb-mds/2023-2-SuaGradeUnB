'use client';

import { useState } from 'react';
import useWindowDimensions from '../hooks/useWindowDimensions';
import useUser from '../hooks/useUser';

import { days, months } from '../utils/dates';

const currentDateObject = new Date(
    new Date().toLocaleString('en', {
        timeZone: 'America/Sao_Paulo'
    })
);

export default function InfoHeader() {
    const { user } = useUser();
    const { breakHeighPoint } = useWindowDimensions();

    const [currentDate, _] = useState(currentDateObject);

    const currentDay = currentDate.getDate().toString();
    const currentMonth = months[currentDate.getMonth()];
    const currentWeekDay = days[currentDate.getDay()];

    return (
        <header className={`
            fixed top-0 w-full 
            rounded-b-[40px] mb-8 flex flex-col z-[5] justify-end bg-primary px-6 
            ${breakHeighPoint ? 'h-24' : 'h-0'} transition-all duration-300
        `}>
            <h1 className='col-span-2 font-semibold text-base text-white'>
                Olá, {user.is_anonymous ? 'Anônimo' : user.first_name}!
            </h1>
            <p className='mb-5 col-span-2 font-medium text-base text-white'>
                {currentWeekDay}, {currentDay} de {currentMonth}
            </p>
        </header>
    );
}