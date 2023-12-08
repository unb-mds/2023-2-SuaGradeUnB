'use client';

import Modal from '@/app/components/Modal/Modal';
import Schedule from '@/app/components/Schedule/Schedule';

import useModal from '@/app/hooks/useModal';
import useSchedules from '@/app/hooks/useSchedules';

import useUser from '@/app/hooks/useUser';

export default function MyGrades() {
    const { localSchedules } = useSchedules();
    const { activeModel } = useModal();
    const { user } = useUser();

    return (
        <>
            {activeModel &&
                <Modal>
                    <Schedule schedules={localSchedules[0]} />
                </Modal>
            }
        </>
    );
}