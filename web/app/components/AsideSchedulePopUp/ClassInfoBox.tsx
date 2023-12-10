import { ClassType, DisciplineType } from '@/app/utils/api/searchDiscipline';
import { HTMLProps, MouseEventHandler, useEffect, useState } from 'react';

import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import ClassInfo from '../ClassInfo';
import Image from 'next/image';

import addIcon from '@/public/icons/add.jpg';

interface ClassInfoBoxPropsType extends HTMLProps<HTMLDivElement> {
    currentDiscipline: DisciplineType,
    currentClass: ClassType,
}

export default function ClassInfoBox({ currentDiscipline, currentClass, ...props }: ClassInfoBoxPropsType) {
    const { classesChange, selectedClasses } = useSelectedClasses();
    const [selected, setSelected] = useState(false);

    useEffect(() => {
        if (selectedClasses.get(currentDiscipline.id)?.has(currentClass.id)) setSelected(true);
        else setSelected(false);
    }, [selectedClasses, classesChange, currentDiscipline, currentClass]);

    return (
        <div
            className={`grid grid-cols-7 ${selected ? 'bg-primary bg-opacity-40' : 'hover:bg-gray-300'} hover:bg-opacity-40 hover:cursor-pointer rounded-md py-1 px-2 ${props.className || ''}`}
        >
            <ClassInfo currentClass={{
                class: currentClass,
                discipline: {
                    id: currentDiscipline.id,
                    name: currentDiscipline.name,
                    code: currentDiscipline.code
                }
            }} />
            <button
                onClick={props.onClick as MouseEventHandler<HTMLButtonElement> | undefined}
                className='hover:cursor-pointer col-start-7 flex justify-center items-center'>
                <Image
                    width={25} height={25}
                    src={addIcon} alt='ícone adicionar matéria'
                />
            </button>
        </div>
    );
}