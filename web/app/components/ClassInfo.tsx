import { Fragment } from 'react';

import { ClassValueType } from '../contexts/SelectedClassesContext/types';
import { FiInfo } from 'react-icons/fi';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogTrigger,
} from './ui/dialog';

interface ClassInfoPropsType {
  currentClass: ClassValueType;
}

export function generateSpecialDates(
  special_dates: Array<Array<string>>,
  days: Array<string>
) {
  return special_dates.map((specialDate, index) => {
    const day = specialDate[0];
    const start = parseInt(specialDate[1]) - 1;
    const end = parseInt(specialDate[2]) - 1;

    function make_days(start: number, end: number) {
      return days.slice(start, end + 1).map((day, index) => (
        <div className="pl-3" key={index}>
          {day}
        </div>
      ));
    }

    return (
      <Fragment key={index}>
        <span className="font-semibold">{day}</span>
        {make_days(start, end)}
      </Fragment>
    );
  });
}

export default function ClassInfo({ currentClass }: ClassInfoPropsType) {
  return (
    <div className="col-span-6">
      <div>
        <span className="font-semibold">Sala:</span>{' '}
        {currentClass.class.classroom}
      </div>
      <div className="flex gap-1 items-center">
        <span className="font-semibold">Horários:</span>{' '}
        {currentClass.class.schedule}
        <Dialog>
          <DialogTrigger aria-label="Informações">
            <FiInfo size={20} />
          </DialogTrigger>
          <DialogContent>
            <DialogTitle>Horários</DialogTitle>
            <DialogDescription>
              {!currentClass.class.special_dates.length
                ? currentClass.class.days.map((day, index) => (
                    <div key={index}>{day}</div>
                  ))
                : generateSpecialDates(
                    currentClass.class.special_dates,
                    currentClass.class.days
                  )}
            </DialogDescription>
          </DialogContent>
        </Dialog>
      </div>
      <div>
        <span className="font-semibold">Professor:</span>{' '}
        {currentClass.class.teachers[0]}{' '}
        {currentClass.class.teachers.length > 1 && 'e outros'}
      </div>
    </div>
  );
}
