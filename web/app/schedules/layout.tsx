'use client';

import { useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import useUser from '@/app/hooks/useUser';

import SelectedClassesContextProvider from '../contexts/SelectedClassesContext';
import ClassesToShowContextProvider from '../contexts/ClassesToShowContext';

import AsideButton from '../components/AsideButton';
import Protected from '../components/Protected';
import { LoadingScreen } from '../components/LoadingScreen';


const days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
const months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

const pathPX = {
    'home': 'left-[18px]',
    'mygrades': 'left-[99px]',
    'profile': 'left-[175px]',
};

const pathPXAnonymous = {
    'home': 'left-[18px]',
    'mygrades': 'left-[132px]'
};

const currentDateObject = new Date(
    new Date().toLocaleString('en', {
        timeZone: 'America/Sao_Paulo'
    })
);

export default function SchedulesLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const { user, isLoading } = useUser();
    const router = useRouter();
    const [currentDate, _] = useState(currentDateObject);
    const path = usePathname().split('/')[2] as keyof typeof pathPX;

    const currentDay = currentDate.getDate().toString();
    const currentMonth = months[currentDate.getMonth()];
    const currentWeekDay = days[currentDate.getDay()];

    if (isLoading) return <LoadingScreen />;

    return (
        <Protected>
            <ClassesToShowContextProvider>
                <SelectedClassesContextProvider>
                    <header className='rounded-b-[40px] mb-8 flex flex-col justify-end bg-primary px-6 h-28'>
                        <h1 className='col-span-2 font-semibold text-base text-white'>
                            Olá, {user.is_anonymous ? 'Anônimo' : user.first_name}!
                        </h1>
                        <p className='mb-5 col-span-2 font-medium text-base text-white'>
                            {currentWeekDay}, {currentDay} de {currentMonth}
                        </p>
                    </header>

                    <main className='pt-5 h-3/5 min-[380px]:h-2/3'>
                        {children}
                    </main>

                    <div className="justify-around flex bg-white rounded-full px-6 py-2 w-[275px] absolute m-auto inset-x-px bottom-8 backdrop-blur-sm bg-opacity-50 drop-shadow-lg">
                        <div
                            className={`bg-primary transition-all duration-300
                    ${user.is_anonymous ? 'w-[120px]' : 'w-[85px]'} h-[50px]
                    rounded-full absolute ${user.is_anonymous ? pathPXAnonymous[path as keyof typeof pathPXAnonymous] : pathPX[path]}`}
                        ></div>
                        <AsideButton icon='Home' text='Home' onClick={() => router.push('/schedules/home')} />
                        <AsideButton icon='calendar_month' text='Grades' onClick={() => router.push('/schedules/mygrades')} />
                        {user.is_anonymous ? null : <AsideButton icon='person' text='Perfil' onClick={() => router.push('/schedules/profile')} />}
                    </div>
                </SelectedClassesContextProvider>
            </ClassesToShowContextProvider>
        </Protected>
    );
}
