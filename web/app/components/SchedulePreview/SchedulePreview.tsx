import { useState } from 'react';
import Image from 'next/image';

import { ScheduleClassType } from '@/app/contexts/SchedulesContext';

import Modal from '../Modal/Modal';
import Schedule from '../Schedule/Schedule';

import uploadIcon from '@/public/icons/upload.jpg';
import downloadIcon from '@/public/icons/download.jpg';
import deleteIcon from '@/public/icons/delete.jpg';

export default function SchedulePreview({ schedule, index }: {
    schedule: Array<ScheduleClassType>;
    index: number;
}) {
    const [activeModel, setActiveModal] = useState(false);

    return (
        <div className='relative w-full max-w-sm'>
            <div
                onClick={() => {
                    if (!activeModel) setActiveModal(true);
                }}
                className='flex justify-center items-center bg-snow-tertiary h-48 rounded-3xl'>
                <Schedule
                    schedules={schedule} preview
                />
                {activeModel &&
                    <Modal setActiveModal={setActiveModal}>
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
                <div className='flex gap-2 h-[25px] opacity-50'>
                    <button>
                        <Image width={25} src={uploadIcon} alt="ícone de upload" />
                    </button>
                    <button>
                        <Image width={25} height={25} src={downloadIcon} alt="ícone de download" />
                    </button>
                    <button>
                        <Image width={25} height={25} src={deleteIcon} alt="ícone de deletar" />
                    </button>
                </div>
            </div>
        </div>
    );
}