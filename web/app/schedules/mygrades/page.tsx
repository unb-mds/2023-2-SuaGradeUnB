'use client';

import useSchedules from '@/app/hooks/useSchedules';

import SchedulePreview from '@/app/components/SchedulePreview/SchedulePreview';

export default function MyGrades() {
    const { localSchedules, cloudSchedules } = useSchedules();

    return (
        <div className='overflow-auto min-h-full max-h-full px-3'>
            <h1 className='text-center text-xl font-semibold pb-6'>Suas Grades</h1>
            <div>
                {localSchedules.length ? <h1 className='text-center pb-5'>Grades locais</h1> : null}
                <div className='flex flex-wrap justify-center items-center gap-10 w-11/12 mx-auto'>
                    {localSchedules.length ?
                        localSchedules.map((schedule, index) =>
                            schedule && <SchedulePreview key={index} index={index} localSchedule={schedule} />
                        ) : null
                    }
                </div>
                {cloudSchedules.length ? <h1 className={`text-center pb-5 ${localSchedules.length ? 'pt-16' : ''}`}>Grades nuvem</h1> : null}
                <div className='flex flex-wrap justify-center items-center gap-10 w-11/12 mx-auto'>
                    {cloudSchedules.length ?
                        cloudSchedules.map((schedule, index) =>
                            schedule && <SchedulePreview key={index} index={index} cloudSchedule={schedule} isCloud />
                        ) : null
                    }
                </div>
            </div>
        </div>
    );
}