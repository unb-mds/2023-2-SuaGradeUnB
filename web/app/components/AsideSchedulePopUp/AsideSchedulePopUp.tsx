import { useEffect, useState } from 'react';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import useShowPopUpContent from '@/app/hooks/useShowPopUpContent';

import { ClassType, DisciplineType } from '@/app/utils/api/searchDiscipline';
import { ClassValueType } from '@/app/contexts/SelectedClassesContext/types';

import DisciplineOptionForm from './Form/DisciplineOptionForm';
import DisciplineFragment from './DisciplineFragment';

import { AsideSchedulePopUpJSXPropsType, AsideSchedulePopUpPropsType, CheckDisciplineObjPropsType } from './types/types';

import _ from 'lodash';

function checkDisciplineObj(props: CheckDisciplineObjPropsType) {
    const { disciplineObj, newSelectedClasses, classId, disciplineId, newClassInfo } = props;

    if (disciplineObj.has(classId)) {
        disciplineObj.delete(classId);

        if (!disciplineObj.size) newSelectedClasses.delete(disciplineId);
    } else disciplineObj.set(classId, newClassInfo);
}

function createNewClassInfo(props: { cls: ClassType, discipline: DisciplineType }) {
    const { cls, discipline } = props;

    return {
        class: cls,
        discipline: {
            id: discipline.id,
            name: discipline.name,
            code: discipline.code
        }
    };
}

function AsideSchedulePopUpJSX(props: AsideSchedulePopUpJSXPropsType) {
    const { showPopUpContent, searchedDisciplineInfos, setSearchedDisciplineInfos, handleSelectClass } = props;

    return (
        <div className='flex justify-center'>
            <div
                ref={props.divAddClassRef}
                className={`fixed flex flex-col justify-between items-center w-11/12 ${showPopUpContent ? 'py-5 h-5/6' : 'h-0'} transition-all duration-500 bottom-0 rounded-t-[40px] bg-snow-secondary z-10`}
            >
                {showPopUpContent &&
                    <section className='flex flex-col items-center gap-5 w-full h-full text-[#333333]'>
                        <DisciplineOptionForm setInfos={setSearchedDisciplineInfos} />
                        <div className='flex flex-col gap-2 w-10/12 overflow-auto h-full'>
                            {searchedDisciplineInfos.map((discipline, index) =>
                                <DisciplineFragment key={index} index={index}
                                    discipline={discipline} disciplineInfos={{ searchedDisciplineInfos, setSearchedDisciplineInfos }}
                                    handleSelectClass={handleSelectClass}
                                />
                            )}
                        </div>
                    </section>
                }
            </div>
        </div >
    );
}

export default function AsideSchedulePopUp(props: AsideSchedulePopUpPropsType) {
    const { showPopUpContent } = useShowPopUpContent();
    const { selectedClasses, setSelectedClasses } = useSelectedClasses();
    const [searchedDisciplineInfos, setSearchedDisciplineInfos] = useState<Array<DisciplineType>>([]);

    useEffect(() => {
        if (!showPopUpContent) setSearchedDisciplineInfos([]);
    }, [showPopUpContent, setSearchedDisciplineInfos]);

    function handleSelectClass(discipline: DisciplineType, cls: ClassType) {
        const disciplineId = discipline.id;
        const classId = cls.id;

        const newSelectedClasses = _.cloneDeep(selectedClasses);
        const disciplineObj = newSelectedClasses.get(disciplineId);

        const newClassInfo = createNewClassInfo({ cls, discipline });

        if (disciplineObj) checkDisciplineObj({ disciplineObj, newSelectedClasses, classId, disciplineId, newClassInfo });
        else {
            const newDiscipline = new Map<number, ClassValueType>();
            newDiscipline.set(classId, newClassInfo);

            newSelectedClasses.set(disciplineId, newDiscipline);
        }

        setSelectedClasses(newSelectedClasses);
    }

    return AsideSchedulePopUpJSX({
        divAddClassRef: props.divAddClassRef,
        showPopUpContent, searchedDisciplineInfos, setSearchedDisciplineInfos,
        handleSelectClass
    });
}