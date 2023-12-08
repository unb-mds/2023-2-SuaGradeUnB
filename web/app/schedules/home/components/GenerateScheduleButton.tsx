'use router';

import { useRouter } from 'next/navigation';
import useClassesToShow from '@/app/hooks/useClassesToShow';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import useSchedules from '@/app/hooks/useSchedules';

import Button from '@/app/components/Button';

import generateSchedule from '@/app/utils/api/generateSchedule';
import { errorToast } from '@/app/utils/errorToast';

export default function GenerateScheduleButton() {
    const router = useRouter();

    const { localSchedules, setLocalSchedules } = useSchedules();
    const { selectedClasses } = useSelectedClasses();
    const { classesToShow } = useClassesToShow();

    return (
        <div className='flex justify-center'>
            <Button
                disabled={!classesToShow.length}
                onClick={async () => {
                    let classes_id = new Array();
                    selectedClasses.forEach((_class) => {
                        Array.from(_class.keys()).forEach((key) => {
                            classes_id.push(key);
                        });
                    });
                    const response = await generateSchedule(classes_id);
                    if (response.status === 200) {
                        setLocalSchedules([
                            ...localSchedules,
                            response.data,
                        ]);
                        router.replace('/schedules/mygrades');
                    } else errorToast('Não foi possível gerar as grades, tente novamente mais tarde!');
                }}
                className='absolute bottom-20 w-52 h-10 font-semibold bg-primary disabled:opacity-70'
            >
                Gerar Grade
            </Button>
        </div>
    );
}