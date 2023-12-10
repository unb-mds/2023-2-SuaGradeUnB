'use router';

import { useRouter } from 'next/navigation';
import useClassesToShow from '@/app/hooks/useClassesToShow';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import useSchedules from '@/app/hooks/useSchedules';

import Button from '@/app/components/Button';

import { ScheduleClassType } from '@/app/contexts/SchedulesContext';

import generateSchedule from '@/app/utils/api/generateSchedule';
import { errorToast } from '@/app/utils/errorToast';

export default function GenerateScheduleButton() {
    const router = useRouter();

    const { setLocalSchedules } = useSchedules();
    const { selectedClasses } = useSelectedClasses();
    const { classesToShow } = useClassesToShow();

    const createSchedule = async () => {
        let classes_id = new Array();
        selectedClasses.forEach((_class) => {
            Array.from(_class.keys()).forEach((key) => {
                classes_id.push(key);
            });
        });
        const response = await generateSchedule(classes_id);
        if (response.status === 200) {
            setLocalSchedules(response.data as Array<ScheduleClassType>);
            router.replace('/schedules/mygrades');
        } else errorToast('Não foi possível gerar as grades, tente novamente mais tarde!');
    };
    return (
        <div className='flex justify-center'>
            <Button disabled={!classesToShow.length} onClick={createSchedule} className='fixed bottom-20 w-52 h-10 font-semibold bg-primary disabled:opacity-70'>
                Gerar Grade
            </Button>
        </div>
    );
}