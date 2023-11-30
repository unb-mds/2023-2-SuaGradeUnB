import { Fragment, LegacyRef, useState } from 'react';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import useShowPopUpContent from '@/app/hooks/useShowPopUpContent';

import { ClassType, DisciplineType } from '@/app/utils/api/searchDiscipline';
import { ClassValueType } from '@/app/contexts/SelectedClassesContext';

import DisciplineOptionForm from './DisciplineOptionForm';
import ClassInfoBox from './ClassInfoBox';

import _ from 'lodash';

interface AsideSchedulePopUpPropsType {
    divAddClassRef?: LegacyRef<HTMLDivElement> | undefined
}

export default function AsideSchedulePopUp(props: AsideSchedulePopUpPropsType) {
    const { showPopUpContent } = useShowPopUpContent();
    const { selectedClasses, setSelectedClasses } = useSelectedClasses();
    const [searchedDisciplineInfos, setSearchedDisciplineInfos] = useState<Array<DisciplineType>>([]);

    function handleDisciplineToggle(index: number) {
        let newInfo: Array<DisciplineType> = [];
        searchedDisciplineInfos.forEach((discipline, number) => {
            if (number != index) newInfo.push({
                ...discipline,
                expanded: false
            });
            else newInfo.push({
                ...discipline,
                expanded: !discipline.expanded
            });
        });

        setSearchedDisciplineInfos(newInfo);
    }

    function handleSelectClass(discipline: DisciplineType, cls: ClassType) {
        const disciplineId = discipline.id;
        const classId = cls.id;

        const newSelectedClasses = _.cloneDeep(selectedClasses);
        const disciplineObj = newSelectedClasses.get(disciplineId);

        const newClassInfo = {
            class: cls,
            discipline: {
                id: discipline.id,
                name: discipline.name,
                code: discipline.code
            }
        };

        if (disciplineObj) {
            if (disciplineObj.has(classId)) {
                disciplineObj.delete(classId);

                if (!disciplineObj.size) newSelectedClasses.delete(disciplineId);
            } else disciplineObj.set(classId, newClassInfo);
        } else {
            const newDiscipline = new Map<number, ClassValueType>();
            newDiscipline.set(classId, newClassInfo);

            newSelectedClasses.set(disciplineId, newDiscipline);
        }

        setSelectedClasses(newSelectedClasses);
    }

    return (
        <div className='flex justify-center'>
            <div
                ref={props.divAddClassRef}
                className={`flex flex-col justify-between items-center w-11/12 ${showPopUpContent ? 'py-5 h-5/6' : 'h-0'} transition-all duration-500 absolute bottom-0 rounded-t-[40px] bg-snow-secondary z-10`}
            >
                {showPopUpContent &&
                    <section className='flex flex-col items-center gap-5 w-full h-full text-[#333333]'>
                        <DisciplineOptionForm setInfos={setSearchedDisciplineInfos} />
                        <div className='flex flex-col gap-2 w-10/12 overflow-auto h-full'>
                            {searchedDisciplineInfos.map((discipline, index) => (
                                <Fragment key={index}>
                                    <button
                                        onClick={() => handleDisciplineToggle(index)}
                                        className='flex items-center gap-3'
                                    >
                                        <span className="material-symbols-rounded">
                                            {discipline.expanded ? 'expand_less' : 'expand_more'}
                                        </span>
                                        <span className='font-semibold'>{discipline.name} - {discipline.code}</span>
                                    </button>
                                    {discipline.expanded &&
                                        <div className='flex flex-col gap-2'>
                                            {discipline.classes.map((cls, index) =>
                                                <ClassInfoBox
                                                    key={index}
                                                    currentClass={cls}
                                                    currentDiscipline={discipline}
                                                    onClick={() => handleSelectClass(discipline, cls)}
                                                />
                                            )}
                                        </div>
                                    }
                                </Fragment>
                            ))}
                        </div>
                    </section>
                }
            </div>
        </div >
    );
}