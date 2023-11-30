'use client';

import { useEffect, useRef } from 'react';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import useClassesToShow from '@/app/hooks/useClassesToShow';

import DisciplineBox from '@/app/components/DisciplineBox';
import AsideSchedulePopUp from '@/app/components/AsideSchedulePopUp/AsideSchedulePopUp';
import GenerateScheduleButton from './components/GenerateScheduleButton';
import AddDisciplineButton from './components/AddDisciplineButton';

import ClickOutsideHandler from './handlers/ClickOutsideHandler';

import ShowPopUpContentContextProvider from '@/app/contexts/ShowPopUpContentContext';

export default function Home() {
    const { classesToShow, setClassesToShow } = useClassesToShow();
    const { classesChange, selectedClasses } = useSelectedClasses();

    const divAddClassRef = useRef(null), buttonAddDisciplineRef = useRef(null);

    useEffect(() => {
        const newClasses = new Array();
        selectedClasses.forEach((cls) => cls.forEach(value => newClasses.push(value)));

        setClassesToShow(newClasses);
    }, [classesChange, selectedClasses, setClassesToShow]);

    return (
        <ShowPopUpContentContextProvider>
            <ClickOutsideHandler refs={{ divAddClassRef, buttonAddDisciplineRef }}>
                <AddDisciplineButton buttonAddDisciplineRef={buttonAddDisciplineRef} />
                <div className={`flex flex-col items-center ${classesToShow.length ? '' : 'justify-center'} gap-5 overflow-auto min-h-full max-h-full pb-2`}>
                    {classesToShow.length ? classesToShow.map((cls, index) =>
                        <DisciplineBox key={index} currentClass={cls} discipline={cls.discipline} />
                    ) : 'Nenhuma disciplina escolhida no momento'}
                </div>

                <AsideSchedulePopUp divAddClassRef={divAddClassRef} />
                <GenerateScheduleButton />
            </ClickOutsideHandler>
        </ShowPopUpContentContextProvider>
    );
}