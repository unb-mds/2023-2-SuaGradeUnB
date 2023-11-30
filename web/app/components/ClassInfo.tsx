import { Fragment } from 'react';

import { ClassValueType } from '../contexts/SelectedClassesContext/types';

import Tooltip from './Tooltip';

interface ClassInfoPropsType {
    currentClass: ClassValueType
}

export default function ClassInfo({ currentClass }: ClassInfoPropsType) {
    return (
        <div>
            <div>
                <span className='font-semibold'>Sala:</span> {currentClass.class.classroom}
            </div>
            <div className='flex gap-1'>
                <span className='font-semibold'>Horários:</span> {currentClass.class.schedule}
                <Tooltip>
                    <div className='flex flex-col gap-1 w-64'>
                        <span className='text-center font-semibold text-lg'>Horários</span>
                        {!currentClass.class.special_dates.length ?
                            currentClass.class.days.map((day, index) =>
                                <div key={index}>
                                    {day}
                                </div>
                            ) : currentClass.class.special_dates.map((specialDate, index) => {
                                const day = specialDate[0];
                                const start = parseInt(specialDate[1]) - 1;
                                const end = parseInt(specialDate[2]) - 1;

                                function make_days(start: number, end: number) {
                                    return currentClass.class.days.slice(start, end + 1).map((day, index) =>
                                        <div className='pl-3' key={index}>
                                            {day}
                                        </div>
                                    );
                                }

                                return (
                                    <Fragment key={index}>
                                        <span className='font-semibold'>
                                            {day}
                                        </span>
                                        {make_days(start, end)}
                                    </Fragment>
                                );
                            })}
                    </div>
                </Tooltip>
            </div>
            <div>
                <span className='font-semibold'>Professor:</span> {currentClass.class.teachers[0]} {currentClass.class.teachers.length > 1 && 'e outros'}
            </div>
        </div>
    );
}