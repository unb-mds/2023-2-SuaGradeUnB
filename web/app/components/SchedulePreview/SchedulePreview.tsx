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
import deleteSchedule from '@/app/utils/api/deleteSchedule';
import { errorToast } from '@/app/utils/errorToast';

import jsPDF from 'jspdf';

const commonError = () => errorToast('Houve um erro na atualização das grades!');

function DeleteButton({
    setActiveDeleteModal,
}: {
    setActiveDeleteModal: (value: boolean) => void;
}) {
    return (
        <button onClick={() => setActiveDeleteModal(true)}>
            <Image width={25} height={25} src={deleteIcon} alt="ícone de deletar" />
        </button>
    );
}

function DeleteModalHandler(props: {
    deleteModal: {
        activeDeleteModal: boolean;
        setActiveDeleteModal: (value: boolean) => void;
    }
    isCloud?: boolean;
    index: number;
    handleDeleteCloud: () => Promise<void>;
}) {
    const { localSchedules, setLocalSchedules } = useSchedules();

    function handleDeleteLocal() {
        const newLocalSchedules = [...localSchedules];
        newLocalSchedules.splice(props.index, 1);
        setLocalSchedules(newLocalSchedules, false);
    }

    async function handleDelete() {
        if (!props.isCloud) handleDeleteLocal();
        else await props.handleDeleteCloud();
        props.deleteModal.setActiveDeleteModal(false);
    }

    return props.deleteModal.activeDeleteModal &&
        <Modal setActiveModal={props.deleteModal.setActiveDeleteModal} noExit>
            <div className="flex flex-col items-center justify-center h-full gap-10">
                <h1 className="font-semibold text-center">A grade será deletada para sempre, tem certeza?</h1>
                <div className="flex gap-16 justify-center mt-4">
                    <Button onClick={() => props.deleteModal.setActiveDeleteModal(false)} className='bg-gray-400'>Não</Button>
                    <Button onClick={() => handleDelete()} className='bg-primary'>Sim</Button>
                </div>
            </div>
        </Modal>;
}

function handleDate(created_at: string) {
    const date = new Date(created_at);

    const currentDay = date.getDate().toString();
    const currentMonth = months[date.getMonth()];
    const currentWeekDay = days[date.getDay()];

    return `${currentWeekDay}, ${currentDay} de ${currentMonth}`;
}

function BottomPart(props: {
    localSchedule?: Array<ScheduleClassType>;
    cloudSchedule?: CloudScheduleType;
    index: number;
    cloud: {
        isCloud?: boolean;
        handleDeleteCloud: () => void;
    }
    setters: {
        setActiveScheduleModal: (value: boolean) => void;
        setActiveDeleteModal: (value: boolean) => void;
        setToDownload: (value: boolean) => void;
    }
}) {
    const { user } = useUser();
    const { setCloudSchedules } = useSchedules();

    const [changeDate, setChangeDate] = useState('');

    async function handleUploadToCloud() {
        const saveResponse = await saveSchedule(props.localSchedule, user.access);

        if (saveResponse.status == 201) {
            getSchedules(user.access).then(response => {
                props.cloud.handleDeleteCloud();
                setCloudSchedules(response.data);
            }).catch(() => commonError());
        } else errorToast('Não foi possível salvar a grade na nuvem!');
    }

    useEffect(() => {
        if (props.cloud.isCloud && props.cloudSchedule?.created_at) {
            setChangeDate(handleDate(props.cloudSchedule.created_at));
        }
    }, [props.cloud.isCloud, props.cloudSchedule?.created_at]);

    return (
        <div className={`flex justify-between items-center w-full absolute ${props.cloud.isCloud ? '-bottom-14' : '-bottom-7'}`}>
            <div
                className='text-[#000000] opacity-40 text-lg font-bold'
            >
                Grade {props.index + 1} <br />
                {props.cloud.isCloud && changeDate && <span className='text-sm font-normal'>{changeDate}</span>}
            </div>
            <div className='flex gap-4 h-[25px] opacity-50'>
                {!props.cloud.isCloud && !user.is_anonymous &&
                    <button onClick={() => handleUploadToCloud()}>
                        <Image width={25} src={uploadIcon} alt="ícone de upload" />
                    </button>
                }
                <button onClick={() => {
                    props.setters.setActiveScheduleModal(true);
                    props.setters.setToDownload(true);
                }}>
                    <Image width={25} height={25} src={downloadIcon} alt="ícone de download" />
                </button>
                <DeleteButton setActiveDeleteModal={props.setters.setActiveDeleteModal} />
            </div>
        </div>
    );
}

function handleDownloadPDF(isCloud: boolean, index: number) {
    const doc = document.getElementById('download-content')!;

    const pdfManager = new jsPDF('l', 'pt', 'a4');
    pdfManager.html(doc, {
        callback: function (doc) {
            doc.save(`schedule-${isCloud ? 'cloud' : 'local'}-${index + 1}.pdf`);
        },
        x: 0, y: 0,
        width: 1150, windowWidth: 2000,
    });
}

export default function SchedulePreview({ localSchedule, cloudSchedule, index, isCloud = false }: {
    localSchedule?: Array<ScheduleClassType>;
    cloudSchedule?: CloudScheduleType;
    index: number;
    isCloud?: boolean;
}) {
    const { user } = useUser();
    const { setCloudSchedules } = useSchedules();

    const [toDownload, setToDownload] = useState(false);
    const [activeScheduleModal, setActiveScheduleModal] = useState(false);
    const [activeDeleteModal, setActiveDeleteModal] = useState(false);

    async function handleDeleteCloud() {
        const response = await deleteSchedule(cloudSchedule?.id, user.access);

        if (response.status == 204) {
            getSchedules(user.access).then(response => {
                setCloudSchedules(response.data);
            }).catch(() => commonError());
        } else errorToast('Não foi possível deletar a grade na nuvem!');
    }

    useEffect(() => {
        if (toDownload && activeScheduleModal) {
            setTimeout(() => {
                handleDownloadPDF(isCloud, index);
                setActiveScheduleModal(false);
                setToDownload(false);
            }, 150);
        }
    }, [toDownload, activeScheduleModal, isCloud, index]);

    return (
        <>
            <div className='relative w-full max-w-sm'>
                <div
                    onClick={() => {
                        if (!activeScheduleModal) setActiveScheduleModal(true);
                    }}
                    className='flex justify-center items-center bg-snow-tertiary h-48 rounded-3xl'>
                    <Schedule schedules={isCloud ? cloudSchedule!.classes : localSchedule} preview />
                    {activeScheduleModal &&
                        <Modal setActiveModal={setActiveScheduleModal}>
                            <Schedule id='download-content' schedules={isCloud ? cloudSchedule!.classes : localSchedule} toDownload={toDownload} />
                        </Modal>
                    }
                </div>
                <BottomPart
                    localSchedule={localSchedule}
                    cloudSchedule={cloudSchedule}
                    index={index}
                    cloud={{ isCloud, handleDeleteCloud }}
                    setters={{ setActiveScheduleModal, setActiveDeleteModal, setToDownload }}
                />
            </div>
            <DeleteModalHandler
                deleteModal={{ activeDeleteModal, setActiveDeleteModal }}
                isCloud={isCloud} index={index} handleDeleteCloud={handleDeleteCloud}
            />
        </>
    );
}