'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import useClassesToShow from '@/app/hooks/useClassesToShow';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import useSchedules from '@/app/hooks/useSchedules';
import useUser from '@/app/hooks/useUser';

import Button from '@/app/components/Button';
import Modal from '@/app/components/Modal/Modal';

import { ScheduleClassType } from '@/app/contexts/SchedulesContext';

import generateSchedule, { EachFieldNumber } from '@/app/utils/api/generateSchedule';
import { errorToast } from '@/app/utils/errorToast';

function PreferenceOrder({ setPreference }: {
    setPreference: (preference: EachFieldNumber) => void
}) {
    return (
        <select className='bg-white shadow-md h-14 p-2 rounded-xl' onChange={(event) => {
            const preference = parseInt(event.target.value) as EachFieldNumber;
            setPreference(preference);
        }}>
            <option value="1">Mínima</option>
            <option value="2">Média</option>
            <option value="3">Máxima</option>
        </select>
    );
}

export default function GenerateScheduleButton() {
    const router = useRouter();

    const { setLoading } = useUser();
    const { setLocalSchedules } = useSchedules();
    const { selectedClasses } = useSelectedClasses();
    const { classesToShow } = useClassesToShow();

    const [activeModal, setActiveModal] = useState(false);
    const [morningPreference, setMorningPreference] = useState<EachFieldNumber>(1);
    const [afternoonPreference, setAfternoonPreference] = useState<EachFieldNumber>(1);
    const [nightPreference, setNightPreference] = useState<EachFieldNumber>(1);

    const createSchedule = () => {
        let classes_id = new Array();
        selectedClasses.forEach((_class) => {
            Array.from(_class.keys()).forEach((key) => {
                classes_id.push(key);
            });
        });

        setLoading(true);
        generateSchedule(classes_id, [morningPreference, afternoonPreference, nightPreference]).then((response) => {
            if (response.status === 200) {
                const schedules = response.data as Array<ScheduleClassType>;

                if (!schedules.length) {
                    errorToast('Nenhuma grade conseguiu ser gerada!');
                    setLoading(false);
                } else {
                    setLocalSchedules(schedules);
                    router.replace('/schedules/mygrades');
                    setTimeout(() => {
                        setLoading(false);
                    }, 500);
                }
            } else {
                errorToast('Não foi possível gerar as grades, tente novamente mais tarde!');
                setLoading(false);
            }
        });
    };

    return (
        <>
            {activeModal &&
                <Modal setActiveModal={setActiveModal} noExit>
                    <div className='flex flex-col justify-center items-center gap-10 p-3 h-full'>
                        <h1 className='font-semibold'>Período de preferência</h1>

                        <div className='flex flex-col gap-3'>
                            <div className='grid grid-cols-3 gap-3 font-medium text-center'>
                                <span>Manhã</span>
                                <span>Tarde</span>
                                <span>Noite</span>
                            </div>
                            <div className='grid grid-cols-3 gap-3'>
                                <PreferenceOrder setPreference={setMorningPreference} />
                                <PreferenceOrder setPreference={setAfternoonPreference} />
                                <PreferenceOrder setPreference={setNightPreference} />
                            </div>
                        </div>

                        <div className='flex gap-16 justify-center items-center'>
                            <Button className='bg-gray-400' onClick={() => setActiveModal(false)}>Cancelar</Button>
                            <Button className='bg-primary' onClick={createSchedule}>Gerar</Button>
                        </div>
                    </div>
                </Modal>
            }
            <div className='flex justify-center'>
                <Button disabled={!classesToShow.length} onClick={() => setActiveModal(true)} className='fixed bottom-20 w-52 h-10 font-semibold bg-primary disabled:opacity-70'>
                    Gerar Grade
                </Button>
            </div>
        </>
    );
}