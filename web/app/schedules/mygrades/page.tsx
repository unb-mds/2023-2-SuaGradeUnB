'use client';

import useSchedules from '@/app/hooks/useSchedules';

import SchedulePreview from '@/app/components/SchedulePreview/SchedulePreview';

function RenderLocalSchedules() {
    const { localSchedules } = useSchedules();
    if (!localSchedules.length) return null;

    return (
        <>
            <h1 className='text-center pb-5'>Grades locais</h1>
            <div className='flex flex-wrap justify-center items-center gap-10 w-11/12 mx-auto'>
                {localSchedules.map((schedule, index) => (
                    schedule && <SchedulePreview key={index} index={index} localSchedule={schedule} position={localSchedules.length - index} />
                ))}
            </div>
        </>

    );
}

function RenderCloudSchedules() {
    const { cloudSchedules } = useSchedules();
    if (!cloudSchedules.length) return null;

    return (
        <>
            <h1 className={`text-center pb-5 ${cloudSchedules.length ? 'pt-16' : ''}`}>Grades nuvem</h1>
            <div className='flex flex-wrap justify-center items-center gap-16 w-11/12 mx-auto'>
                {cloudSchedules.map((schedule, index) => (
                    schedule && <SchedulePreview key={index} index={index} cloudSchedule={schedule} position={cloudSchedules.length - index} isCloud />
                ))}
            </div>
        </>
    );
}

export default function MyGrades() {
    const { localSchedules, cloudSchedules } = useSchedules();

    return (
        <div className='overflow-auto min-h-full max-h-full px-3'>
            <h1 className='text-center text-xl font-semibold pb-6'>Suas Grades</h1>
            <RenderLocalSchedules />
            <RenderCloudSchedules />
            {localSchedules.length === 0 && cloudSchedules.length === 0 && (
                <div className='flex h-full justify-center items-center'>
                    Você ainda não possui nenhuma grade.
                </div>
            )}
        </div>
    );
}