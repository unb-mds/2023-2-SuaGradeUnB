import { Dispatch, LegacyRef, SetStateAction } from 'react';

import { ClassType, DisciplineType } from '@/app/utils/api/searchDiscipline';
import { ClassValueType } from '@/app/contexts/SelectedClassesContext/types';

export interface FormType {
    formData: FormData,
    setFormData: Dispatch<SetStateAction<FormData>>,
}

export interface InputFormPropsType {
    form: FormType
    setInfos: Dispatch<SetStateAction<Array<DisciplineType>>>
}

export interface DisciplineOptionFormPropsType {
    setInfos: Dispatch<SetStateAction<Array<DisciplineType>>>
}

export interface FormData {
    search: string,
    year: string,
    period: string
}

export const defaultFormData: FormData = {
    search: '',
    year: '',
    period: ''
};

export interface AsideSchedulePopUpPropsType {
    divAddClassRef?: LegacyRef<HTMLDivElement> | undefined
}

export interface CheckDisciplineObjPropsType {
    disciplineObj: Map<number, ClassValueType>,
    newSelectedClasses: Map<number, Map<number, ClassValueType>>,
    classId: number,
    disciplineId: number,
    newClassInfo: ClassValueType
}

export interface AsideSchedulePopUpJSXPropsType {
    divAddClassRef?: LegacyRef<HTMLDivElement> | undefined,
    showPopUpContent: boolean,
    searchedDisciplineInfos: Array<DisciplineType>,
    setSearchedDisciplineInfos: React.Dispatch<React.SetStateAction<DisciplineType[]>>
    handleSelectClass: (discipline: DisciplineType, cls: ClassType) => void
}