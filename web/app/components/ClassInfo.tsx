import { ClassValueType } from '../contexts/SelectedClassesContext';
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
                    {currentClass.class.days.map((day, index) =>
                        <div key={index}>
                            {day}
                        </div>
                    )}
                </Tooltip>
            </div>
            <div>
                <span className='font-semibold'>Professor:</span> {currentClass.class.teachers[0]} {currentClass.class.teachers.length > 1 && 'e outros'}
            </div>
        </div>
    );
}