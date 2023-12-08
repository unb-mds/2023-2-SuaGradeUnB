import { useState } from 'react';
import useSchedules from '@/app/hooks/useSchedules';

import { ScheduleClassType } from '@/app/contexts/SchedulesContext';

import Image from 'next/image';

import Modal from '../Modal/Modal';
import Schedule from '../Schedule/Schedule';

import uploadIcon from '@/public/icons/upload.jpg';
import downloadIcon from '@/public/icons/download.jpg';
import deleteIcon from '@/public/icons/delete.jpg';
import Button from '../Button';

export default function SchedulePreview({ schedule, index, isCloud = false }: {
    schedule: Array<ScheduleClassType>;
    index: number;
    isCloud?: boolean;
}) {
    const { localSchedules, setLocalSchedules } = useSchedules();

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

    return (
        <>
            <div className='relative w-full max-w-sm'>
                <div
                    onClick={() => {
                        if (!activeScheduleModal) setActiveScheduleModal(true);
                    }}
                    className='flex justify-center items-center bg-snow-tertiary h-48 rounded-3xl'>
                    <Schedule
                        schedules={schedule} preview
                    />
                    {activeScheduleModal &&
                        <Modal setActiveModal={setActiveScheduleModal}>
                            <Schedule schedules={schedule} />
                        </Modal>
                    }
                </div>
                <div className='flex justify-between items-center w-full absolute -bottom-7'>
                    <div
                        className='text-[#000000] opacity-40 text-lg font-bold'
                    >
                        Grade {index + 1}
                    </div>
                    <div className='flex gap-4 h-[25px] opacity-50'>
                        <button>
                            <Image width={25} src={uploadIcon} alt="ícone de upload" />
                        </button>
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