import { ClassValueType } from '../contexts/SelectedClassesContext';
import useSelectedClasses from '../hooks/useSelectedClasses';
import ClassInfo from './ClassInfo';

interface DisciplineBoxPropsType {
    currentClass: ClassValueType
    discipline: {
        id: number,
        name: string,
        code: string
    }
}

export default function DisciplineBox({ currentClass, discipline }: DisciplineBoxPropsType) {
    const { selectedClasses, setSelectedClasses } = useSelectedClasses();

    function handleDeleteClass() {
        const newSelectedClasses = selectedClasses;
        newSelectedClasses.get(discipline.id)?.delete(currentClass.class.id);
        setSelectedClasses(newSelectedClasses);
    }

    return (
        <span className='flex justify-between rounded-lg w-10/12 py-2 px-4 shadow-lg bg-snow-primary'>
            <div>
                <section>
                    <span className='font-semibold'>Disciplina: </span> {discipline.name} - {discipline.code}
                </section>
                <ClassInfo currentClass={currentClass} />
            </div>
            <button onClick={handleDeleteClass} className='material-symbols-rounded hover:text-red-900'>
                delete
            </button>
        </span>
    );
}