import Image from 'next/image';

import { ClassValueType } from '../contexts/SelectedClassesContext/types';

import useSelectedClasses from '../hooks/useSelectedClasses';

import ClassInfo from './ClassInfo';

import deleteIcon from '../../public/icons/delete.jpg';

import { FiTrash2 } from 'react-icons/fi';

import _ from 'lodash';

interface DisciplineBoxPropsType {
  currentClass: ClassValueType;
  discipline: {
    id: number;
    name: string;
    code: string;
  };
}

export default function DisciplineBox({
  currentClass,
  discipline,
}: DisciplineBoxPropsType) {
  const { selectedClasses, setSelectedClasses } = useSelectedClasses();

  function handleDeleteClass() {
    const newSelectedClasses = _.cloneDeep(selectedClasses);
    newSelectedClasses.get(discipline.id)?.delete(currentClass.class.id);
    if (!newSelectedClasses.get(discipline.id)?.size) {
      newSelectedClasses.delete(discipline.id);
    }
    setSelectedClasses(newSelectedClasses);
  }

  return (
    <span className="relative flex justify-between rounded-lg w-10/12 py-2 pl-4 pr-8 shadow-lg bg-snow-primary">
      <div>
        <section>
          <span className="font-semibold">Código: </span> {discipline.code}
        </section>
        <ClassInfo currentClass={currentClass} />
      </div>
      <button
        onClick={handleDeleteClass}
        // className="absolute right-1 top-0 bottom-0 my-auto"
      >
        <FiTrash2 size={24} />
        {/* <Image height={24} width={24} src={deleteIcon} alt="deletar" /> */}
      </button>
    </span>
  );
}
