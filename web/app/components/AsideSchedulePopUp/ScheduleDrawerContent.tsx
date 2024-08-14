import { useEffect, useState } from 'react';
import DisciplineOptionForm from './Form/DisciplineOptionForm';
import { ClassType, DisciplineType } from '@/app/utils/api/searchDiscipline';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import { CheckDisciplineObjPropsType } from './types/types';
import { ClassValueType } from '@/app/contexts/SelectedClassesContext/types';
import _ from 'lodash';
import DisciplineFragment from './DisciplineFragment';

export const ScheduleDrawerContent = () => {
  const { selectedClasses, setSelectedClasses } = useSelectedClasses();
  const [searchedDisciplines, setSearchedDisciplines] = useState<
    Array<DisciplineType>
  >([]);

  function handleSelectClass(discipline: DisciplineType, cls: ClassType) {
    const disciplineId = discipline.id;
    const classId = cls.id;

    const newSelectedClasses = _.cloneDeep(selectedClasses);

    const disciplineObj = newSelectedClasses.get(disciplineId);

    const newClassInfo = createNewClassInfo({ cls, discipline });

    if (disciplineObj)
      checkDisciplineObj({
        disciplineObj,
        newSelectedClasses,
        classId,
        disciplineId,
        newClassInfo,
      });
    else {
      const newDiscipline = new Map<number, ClassValueType>();
      newDiscipline.set(classId, newClassInfo);

      newSelectedClasses.set(disciplineId, newDiscipline);
    }

    setSelectedClasses(newSelectedClasses);
  }

  return (
    <div className="flex justify-center mt-6 px-2">
      <section className="flex flex-col items-center gap-5 w-full h-full text-gray-700">
        <DisciplineOptionForm setInfos={setSearchedDisciplines} />
        <div
          className="flex flex-col gap-2 w-10/12 overflow-auto h-full max-h-[50vh]"
          data-vaul-no-drag
        >
          {searchedDisciplines.map((discipline, index) => (
            <DisciplineFragment
              key={index}
              index={index}
              discipline={discipline}
              disciplineInfos={{
                searchedDisciplineInfos: searchedDisciplines,
                setSearchedDisciplineInfos: setSearchedDisciplines,
              }}
              handleSelectClass={handleSelectClass}
            />
          ))}
        </div>
      </section>
    </div>
  );
};

function createNewClassInfo(props: {
  cls: ClassType;
  discipline: DisciplineType;
}) {
  const { cls, discipline } = props;

  return {
    class: cls,
    discipline: {
      id: discipline.id,
      name: discipline.name,
      code: discipline.code,
    },
  };
}

function checkDisciplineObj(props: CheckDisciplineObjPropsType) {
  const {
    disciplineObj,
    newSelectedClasses,
    classId,
    disciplineId,
    newClassInfo,
  } = props;

  if (disciplineObj.has(classId)) {
    disciplineObj.delete(classId);

    if (!disciplineObj.size) newSelectedClasses.delete(disciplineId);
  } else disciplineObj.set(classId, newClassInfo);
}
