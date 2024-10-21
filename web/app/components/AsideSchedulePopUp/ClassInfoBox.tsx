import { ClassType, DisciplineType } from '@/app/utils/api/searchDiscipline';
import { HTMLProps, MouseEventHandler, useEffect, useState } from 'react';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import ClassInfo from '../ClassInfo';
import { twMerge } from 'tailwind-merge';
import { FiPlus, FiMinus } from 'react-icons/fi';

interface ClassInfoBoxPropsType extends HTMLProps<HTMLDivElement> {
  currentDiscipline: DisciplineType;
  currentClass: ClassType;
}

export default function ClassInfoBox({
  currentDiscipline,
  currentClass,
  ...props
}: ClassInfoBoxPropsType) {
  const { classesChange, selectedClasses } = useSelectedClasses();
  const [selected, setSelected] = useState(false);

  useEffect(() => {
    if (selectedClasses.get(currentDiscipline.id)?.has(currentClass.id))
      setSelected(true);
    else setSelected(false);
  }, [selectedClasses, classesChange, currentDiscipline, currentClass]);

  return (
    <div
      className={twMerge(
        'grid grid-cols-7 hover:bg-opacity-40 hover:cursor-pointer rounded-md py-1 px-2',
        selected ? 'bg-primary/40' : 'hover:bg-gray-300',
        props.className
      )}
    >
      <ClassInfo
        currentClass={{
          class: currentClass,
          discipline: {
            id: currentDiscipline.id,
            name: currentDiscipline.name,
            code: currentDiscipline.code,
          },
        }}
      />
      <button
        onClick={
          props.onClick as MouseEventHandler<HTMLButtonElement> | undefined
        }
        aria-label="Selecionar/Desselecionar aula"
        className="hover:cursor-pointer col-start-7 flex justify-center items-center"
      >
        {selected ? <FiMinus size={24} /> : <FiPlus size={24} />}
      </button>
    </div>
  );
}
