'use client';

import { Fragment, useEffect, useRef } from 'react';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import useClassesToShow from '@/app/hooks/useClassesToShow';

import DisciplineBox from '@/app/components/DisciplineBox';
import AsideSchedulePopUp from '@/app/components/AsideSchedulePopUp/AsideSchedulePopUp';
import GenerateScheduleButton from './components/GenerateScheduleButton';
import AddDisciplineButton from './components/AddDisciplineButton';

import ClickOutsideHandler from './handlers/ClickOutsideHandler';

import ShowPopUpContentContextProvider from '@/app/contexts/ShowPopUpContentContext';

import { ClassValueType } from '@/app/contexts/SelectedClassesContext/types';

function DisciplineBlockJSX({ ...props }: {
    index: number,
    cls: ClassValueType,
    classesToShow: ClassValueType[]
}) {
    let classAppearance;
    for (let indexInner = 0; indexInner < props.classesToShow.length; indexInner++) {
        if (props.classesToShow[indexInner].discipline.code === props.cls.discipline.code) {
            classAppearance = indexInner;
            break;
        }
    }

    return (
        <Fragment key={props.index}>
            {props.index === classAppearance &&
                <span className='flex justify-center items-center text-center rounded-md font-medium bg-primary bg-opacity-80 w-10/12 p-2'>
                    {props.cls.discipline.name}
                </span>
            }
            <DisciplineBox currentClass={props.cls} discipline={props.cls.discipline} />
        </Fragment>
    );
}

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
                <div className={`flex flex-col items-center ${classesToShow.length ? '' : 'justify-center text-center'} gap-5 overflow-auto min-h-full max-h-full pb-2`}>
                    {classesToShow.length ? classesToShow.map((cls, index) => {
                        return DisciplineBlockJSX({ index, cls, classesToShow });
                    }) : 'Nenhuma disciplina escolhida no momento'}
                </div>

                <AsideSchedulePopUp divAddClassRef={divAddClassRef} />
                <GenerateScheduleButton />
            </ClickOutsideHandler>
        </ShowPopUpContentContextProvider>
    );
}