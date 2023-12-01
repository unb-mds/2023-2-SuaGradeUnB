import { ClassType } from '@/app/utils/api/searchDiscipline';

export type ClassValueType = {
    class: ClassType,
    discipline: {
        id: number,
        name: string,
        code: string
    }
}
export type SelectedClassesType = Map<number, Map<number, ClassValueType>>;

export interface SelectedClassesContextType {
    classesChange: boolean,
    selectedClasses: SelectedClassesType,
    setSelectedClasses: (value: SelectedClassesType) => void;
    currentYearPeriod: string,
    setCurrentYearPeriod: (string: string) => void
}

export interface SelectedClassesContextProviderPropsType {
    children: React.ReactNode
}

export interface ProviderJSXPropsType {
    children: React.ReactNode;

    classesChange: boolean;
    selectedClasses: SelectedClassesType;
    setSelectedClasses: (value: SelectedClassesType) => void;
    currentYearPeriod: string;
    setCurrentYearPeriod: (value: string) => void;
}
