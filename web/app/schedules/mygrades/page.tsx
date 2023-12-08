'use client';

import useSchedules from '@/app/hooks/useSchedules';

import SchedulePreview from '@/app/components/SchedulePreview/SchedulePreview';

export default function MyGrades() {
    const { localSchedules } = useSchedules();

    return (
        <div className='overflow-auto min-h-full max-h-full px-3'>
            <div className='flex flex-wrap justify-center items-center gap-10 w-11/12 mx-auto'>
                {localSchedules.map((schedule, index) =>
                    schedule && <SchedulePreview key={index} index={index} schedule={schedule} />
                )}
            </div>
        </div>
    );
}