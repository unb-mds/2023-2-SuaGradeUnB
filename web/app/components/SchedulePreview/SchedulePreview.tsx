'use client';

import { useEffect, useState } from 'react';
import useSchedules from '@/app/hooks/useSchedules';
import useUser from '@/app/hooks/useUser';

import { CloudScheduleType, ScheduleClassType } from '@/app/contexts/SchedulesContext';

import Image from 'next/image';
import Modal from '../Modal/Modal';
import Schedule from '../Schedule/Schedule';
import Button from '../Button';

import uploadIcon from '@/public/icons/upload.jpg';
import downloadIcon from '@/public/icons/download.jpg';
import deleteIcon from '@/public/icons/delete.jpg';
import saveSchedule from '@/app/utils/api/saveSchedule';
import getSchedules from '@/app/utils/api/getSchedules';
import { days, months } from '@/app/utils/dates';

export default function SchedulePreview({ localSchedule, cloudSchedule, index, isCloud = false }: {
    localSchedule?: Array<ScheduleClassType>;
    cloudSchedule?: CloudScheduleType;
    index: number;
    isCloud?: boolean;
}) {
    const { user } = useUser();
    const { localSchedules, setLocalSchedules, setCloudSchedules } = useSchedules();

    const [changeDate, setChangeDate] = useState('');
    const [activeScheduleModal, setActiveScheduleModal] = useState(false);
    const [activeDeleteModal, setActiveDeleteModal] = useState(false);

    function handleDelete() {
        if (!isCloud) {
            const newLocalSchedules = [...localSchedules];
            newLocalSchedules.splice(index, 1);
            setLocalSchedules(newLocalSchedules, false);
        }
        setActiveDeleteModal(false);
    }

    async function handleUploadToCloud() {
        const saveResponse = await saveSchedule(localSchedule, user.access);
        const getResponse = await getSchedules(user.access);

        if (saveResponse.status == 201 && getResponse.status == 200) {
            const data: Array<any> = getResponse.data;
            data.forEach((schedule, index) => {
                data[index].classes = JSON.parse(schedule.classes);
            });
            handleDelete();
            setCloudSchedules(data);
        }
    }

    useEffect(() => {
        if (isCloud && cloudSchedule?.created_at) {
            const date = new Date(cloudSchedule.created_at);

            const currentDay = date.getDate().toString();
            const currentMonth = months[date.getMonth()];
            const currentWeekDay = days[date.getDay()];

            setChangeDate(`${currentWeekDay}, ${currentDay} de ${currentMonth}`);
        }
    }, [isCloud, cloudSchedule?.created_at]);

    return (
        <>
            <div className='relative w-full max-w-sm'>
                <div
                    onClick={() => {
                        if (!activeScheduleModal) setActiveScheduleModal(true);
                    }}
                    className='flex justify-center items-center bg-snow-tertiary h-48 rounded-3xl'>
                    <Schedule
                        schedules={isCloud ? cloudSchedule!.classes : localSchedule} preview
                    />
                    {activeScheduleModal &&
                        <Modal setActiveModal={setActiveScheduleModal}>
                            <Schedule schedules={isCloud ? cloudSchedule!.classes : localSchedule} />
                        </Modal>
                    }
                </div>
                <div className='flex justify-between items-center w-full absolute -bottom-7'>
                    <div
                        className='text-[#000000] opacity-40 text-lg font-bold'
                    >
                        Grade {index + 1}
                        {isCloud && changeDate && <span className='text-sm font-normal'> - {changeDate}</span>}
                    </div>
                    <div className='flex gap-4 h-[25px] opacity-50'>
                        {!isCloud &&
                            <button onClick={() => handleUploadToCloud()}>
                                <Image width={25} src={uploadIcon} alt="ícone de upload" />
                            </button>
                        }
                        <button>
                            <Image width={25} height={25} src={downloadIcon} alt="ícone de download" />
                        </button>
                        <button onClick={() => setActiveDeleteModal(true)}>
                            <Image width={25} height={25} src={deleteIcon} alt="ícone de deletar" />
                        </button>
                    </div>
                </div>
            </div>
            {activeDeleteModal &&
                <Modal setActiveModal={setActiveDeleteModal} noExit>
                    <div className="flex flex-col items-center justify-center h-full gap-10">
                        <h1 className="font-semibold text-center">A grade será deletada para sempre, tem certeza?</h1>
                        <div className="flex gap-16 justify-center mt-4">
                            <Button onClick={() => setActiveDeleteModal(false)} className='bg-gray-400'>
                                Não
                            </Button>
                            <Button onClick={() => handleDelete()} className='bg-primary'>
                                Sim
                            </Button>
                        </div>
                    </div>
                </Modal>
            }
        </>
    );
}