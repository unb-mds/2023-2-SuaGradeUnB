import type { ClassType, DisciplineType } from '../../utils/api/searchDiscipline';
import request from '../../utils/request';
import { settings } from '../../utils/settings';
import type { ClassValueType, SelectedClassesType } from './types';

export const DRAFT_KEY = 'suagrade:selected-classes:v1';
export const MAX_CLASSES = 4;
export const MAX_DISCIPLINES = 11;

export type Selection = { selectedClasses: SelectedClassesType; currentYearPeriod: string };
type DraftDiscipline = { id: number; code: string; classIds: number[] };
type Draft = { version: 1; yearPeriod: string; disciplines: DraftDiscipline[] };

const isRecord = (value: unknown): value is Record<string, unknown> =>
    typeof value === 'object' && value !== null;
const isId = (value: unknown): value is number => Number.isSafeInteger(value) && Number(value) > 0;
const isStrings = (value: unknown): value is string[] =>
    Array.isArray(value) && value.every(item => typeof item === 'string');

function isDraft(value: unknown): value is Draft {
    if (!isRecord(value) || value.version !== 1 || typeof value.yearPeriod !== 'string' ||
        !/^\d{4}\/\d{1,2}$/.test(value.yearPeriod) || !Array.isArray(value.disciplines) ||
        !value.disciplines.length || value.disciplines.length > MAX_DISCIPLINES) return false;

    const ids = new Set<number>();
    return value.disciplines.every(item => {
        if (!isRecord(item) || !isId(item.id) || ids.has(item.id) || typeof item.code !== 'string' ||
            item.code.trim().length < 4 || !Array.isArray(item.classIds) || !item.classIds.length ||
            item.classIds.length > MAX_CLASSES || !item.classIds.every(isId) ||
            new Set(item.classIds).size !== item.classIds.length) return false;
        ids.add(item.id);
        return true;
    });
}

export function clearDraft() {
    try { sessionStorage.removeItem(DRAFT_KEY); } catch { /* Storage may be disabled. */ }
}

export function readDraft(): Draft | null {
    try {
        const raw = sessionStorage.getItem(DRAFT_KEY);
        if (raw === null) return null;
        const draft: unknown = JSON.parse(raw);
        if (isDraft(draft)) return draft;
    } catch { /* Invalid JSON or unavailable storage must not break the page. */ }
    clearDraft();
    return null;
}

export function saveDraft({ selectedClasses, currentYearPeriod }: Selection) {
    if (!selectedClasses.size || !currentYearPeriod) {
        clearDraft();
        return;
    }
    const disciplines = Array.from(selectedClasses, ([id, classes]) => ({
        id, code: classes.values().next().value!.discipline.code, classIds: Array.from(classes.keys())
    }));
    try {
        sessionStorage.setItem(DRAFT_KEY, JSON.stringify({ version: 1, yearPeriod: currentYearPeriod, disciplines }));
    } catch { /* Keep in-memory selection usable if storage is blocked or full. */ }
}

function isClass(value: unknown): value is ClassType {
    return isRecord(value) && isId(value.id) && typeof value._class === 'string' &&
        typeof value.classroom === 'string' && typeof value.schedule === 'string' &&
        isStrings(value.days) && isStrings(value.teachers) && Array.isArray(value.special_dates) &&
        value.special_dates.every(isStrings);
}

// Only identifiers are stored. Names, rooms, teachers and schedules always come from the API.
export async function restoreDraft(draft: Draft): Promise<Selection> {
    const [year, period] = draft.yearPeriod.split('/');
    const restored = await Promise.all(draft.disciplines.map(async saved => {
        const { data } = await request.get<unknown>('/courses/', {
            ...settings, params: { search: saved.code, year, period }, timeout: 10000
        });
        if (!Array.isArray(data)) throw new Error('Invalid courses response');
        const discipline = data.find((item: unknown): item is DisciplineType => isRecord(item) &&
            item.id === saved.id && item.code === saved.code && typeof item.name === 'string' &&
            Array.isArray(item.classes));
        const classes = new Map<number, ClassValueType>();
        if (discipline) {
            saved.classIds.forEach(id => {
                const cls = discipline.classes.find(item => isClass(item) && item.id === id);
                if (cls) classes.set(id, {
                    class: cls,
                    discipline: { id: discipline.id, name: discipline.name, code: discipline.code }
                });
            });
        }
        return [saved.id, classes] as const;
    }));
    const selectedClasses = new Map(restored.filter(([, classes]) => classes.size));
    return { selectedClasses, currentYearPeriod: selectedClasses.size ? draft.yearPeriod : '' };
}
