'use client';

import { useEffect, useState } from 'react';
import useSchedules from '@/app/hooks/useSchedules';
import useUser from '@/app/hooks/useUser';

import {
  CloudScheduleType,
  ScheduleClassType,
} from '@/app/contexts/SchedulesContext';

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
import { errorToast, successToast } from '@/app/utils/toast';

import jsPDF from 'jspdf';
import { AxiosError } from 'axios';
import { FiCloud, FiDownload, FiTrash2, FiUploadCloud } from 'react-icons/fi';
import { Tooltip, TooltipContent, TooltipTrigger } from '../ui/tooltip';

const commonError = () =>
  errorToast('Houve um erro na atualização das grades!');

function DeleteButton({
  setActiveDeleteModal,
}: {
  setActiveDeleteModal: (value: boolean) => void;
}) {
  return (
    <Tooltip>
      <TooltipTrigger>
        <button onClick={() => setActiveDeleteModal(true)}>
          <FiTrash2 size={24} className="opacity-50" />
        </button>
      </TooltipTrigger>
      <TooltipContent sideOffset={5} align="center">
        Deletar
      </TooltipContent>
    </Tooltip>
  );
}

function DeleteModalHandler(props: {
  deleteModal: {
    activeDeleteModal: boolean;
    setActiveDeleteModal: (value: boolean) => void;
  };
  isCloud?: boolean;
  index: number;
  deleteHandler: {
    handleDeleteCloud: () => Promise<void>;
    handleDeleteLocal: () => void;
  };
}) {
  async function handleDelete() {
    if (!props.isCloud) props.deleteHandler.handleDeleteLocal();
    else await props.deleteHandler.handleDeleteCloud();
    props.deleteModal.setActiveDeleteModal(false);
  }

  return (
    props.deleteModal.activeDeleteModal && (
      <Modal setActiveModal={props.deleteModal.setActiveDeleteModal} noExit>
        <div className="flex flex-col items-center justify-center h-full gap-10">
          <h1 className="font-semibold text-center">
            A grade será deletada para sempre, tem certeza?
          </h1>
          <div className="flex gap-16 justify-center mt-4">
            <Button
              onClick={() => props.deleteModal.setActiveDeleteModal(false)}
              className="bg-gray-400"
            >
              Não
            </Button>
            <Button onClick={() => handleDelete()} className="bg-primary">
              Sim
            </Button>
          </div>
        </div>
      </Modal>
    )
  );
}

function handleDate(created_at: string) {
  const date = new Date(created_at);

  const currentDay = date.getDate().toString();
  const currentMonth = months[date.getMonth()];
  const currentWeekDay = days[date.getDay()];

  return `${currentWeekDay}, ${currentDay} de ${currentMonth}`;
}

function BottomPart(props: {
  schedules: {
    localSchedule?: Array<ScheduleClassType>;
    cloudSchedule?: CloudScheduleType;
  };
  index: number;
  position: number;
  isCloud?: boolean;
  handleDelete: () => void;
  setters: {
    setActiveScheduleModal: (value: boolean) => void;
    setActiveDeleteModal: (value: boolean) => void;
    setToDownload: (value: boolean) => void;
  };
}) {
  const { user } = useUser();

  const [changeDate, setChangeDate] = useState('');

  useEffect(() => {
    if (props.isCloud && props.schedules.cloudSchedule?.created_at) {
      setChangeDate(handleDate(props.schedules.cloudSchedule.created_at));
    }
  }, [props.isCloud, props.schedules.cloudSchedule?.created_at]);

  return (
    <div
      className={`flex justify-between items-center w-full ${
        props.isCloud ? '-bottom-14' : '-bottom-7'
      }`}
    >
      <div className="mt-3">
        <p className="text-black opacity-40 text-lg font-bold">
          Grade {props.position}
        </p>
        {props.isCloud && changeDate && (
          <p className="text-sm font-normal opacity-40">{changeDate}</p>
        )}
      </div>
      <div className="flex gap-4 h-[25px]">
        {!props.isCloud && !user.is_anonymous && (
          <UploadToCloudButton
            schedules={props.schedules}
            handleDelete={props.handleDelete}
          />
        )}
        <Tooltip>
          <TooltipTrigger>
            <button
              onClick={() => {
                props.setters.setActiveScheduleModal(true);
                props.setters.setToDownload(true);
              }}
            >
              <FiDownload size={24} className="opacity-50" />
            </button>
          </TooltipTrigger>
          <TooltipContent sideOffset={5} align="center">
            Baixar
          </TooltipContent>
        </Tooltip>
        <DeleteButton
          setActiveDeleteModal={props.setters.setActiveDeleteModal}
        />
      </div>
    </div>
  );
}

function UploadToCloudButton({
  ...props
}: {
  schedules: {
    localSchedule?: Array<ScheduleClassType>;
  };
  handleDelete: () => void;
}) {
  const { user } = useUser();
  const { setCloudSchedules } = useSchedules();

  function handleSuccessToSave() {
    getSchedules(user.access)
      .then((response) => {
        props.handleDelete();
        setCloudSchedules(response.data);
      })
      .catch(() => commonError());
    successToast('Grade salva com sucesso!');
  }

  function handleErrorToSave(axiosError: AxiosError) {
    if (axiosError.response) {
      const data = axiosError.response.data as { errors: string };
      errorToast(data.errors);
    }
  }

  /**
   * Tenta salvar a grade na nuvem, se der certo, atualiza as grades locais.
   * Caso contrário, exibe errorToast com mensagem retornada pela API.
   */
  async function handleUploadToCloud() {
    saveSchedule(props.schedules.localSchedule, user.access)
      .then((response) => {
        if (response.status == 201) handleSuccessToSave();
      })
      .catch((error: any) => handleErrorToSave(error));
  }

  return (
    <Tooltip>
      <TooltipTrigger>
        <button onClick={() => handleUploadToCloud()}>
          <FiUploadCloud size={24} className="opacity-50" />
        </button>
      </TooltipTrigger>
      <TooltipContent sideOffset={5} align="center">
        Salvar na nuvem
      </TooltipContent>
    </Tooltip>
  );
}

function handleDownloadPDF(isCloud: boolean, index: number) {
  const doc = document.getElementById('download-content')!;

  const pdfManager = new jsPDF('l', 'pt', 'a4');
  pdfManager.html(doc, {
    callback: function (doc) {
      doc.save(`schedule-${isCloud ? 'cloud' : 'local'}-${index + 1}.pdf`);
    },
    x: 0,
    y: 0,
    width: 1150,
    windowWidth: 2000,
  });
}

export default function SchedulePreview({
  localSchedule,
  cloudSchedule,
  index,
  position,
  isCloud = false,
}: {
  localSchedule?: Array<ScheduleClassType>;
  cloudSchedule?: CloudScheduleType;
  index: number;
  position: number;
  isCloud?: boolean;
}) {
  const { user } = useUser();
  const { localSchedules, setCloudSchedules, setLocalSchedules } =
    useSchedules();

  const [toDownload, setToDownload] = useState(false);
  const [activeScheduleModal, setActiveScheduleModal] = useState(false);
  const [activeDeleteModal, setActiveDeleteModal] = useState(false);

  async function handleDeleteCloud() {
    const response = await deleteSchedule(cloudSchedule?.id, user.access);

    if (response.status == 204) {
      getSchedules(user.access)
        .then((response) => {
          setCloudSchedules(response.data);
        })
        .catch(() => commonError());
    } else errorToast('Não foi possível deletar a grade na nuvem!');
  }

  function handleDeleteLocal() {
    const newLocalSchedules = [...localSchedules];
    newLocalSchedules.splice(index, 1);
    setLocalSchedules(newLocalSchedules, false);
  }

  useEffect(() => {
    if (toDownload && activeScheduleModal) {
      setTimeout(() => {
        handleDownloadPDF(isCloud, index);
        setActiveScheduleModal(false);
        setToDownload(false);
      }, 75);
    }
  }, [toDownload, activeScheduleModal, isCloud, index]);

  return (
    <>
      <div className="relative w-full max-w-sm">
        <div
          onClick={() => {
            if (!activeScheduleModal) setActiveScheduleModal(true);
          }}
          className="flex justify-center items-center bg-snow-tertiary h-48 rounded-3xl"
        >
          <Schedule
            schedules={isCloud ? cloudSchedule!.classes : localSchedule}
            preview
          />
          {activeScheduleModal && (
            <Modal setActiveModal={setActiveScheduleModal}>
              <Schedule
                id="download-content"
                schedules={isCloud ? cloudSchedule!.classes : localSchedule}
                toDownload={toDownload}
              />
            </Modal>
          )}
        </div>
        <BottomPart
          schedules={{ localSchedule, cloudSchedule }}
          index={index}
          position={position}
          isCloud={isCloud}
          setters={{
            setActiveScheduleModal,
            setActiveDeleteModal,
            setToDownload,
          }}
          handleDelete={handleDeleteLocal}
        />
      </div>
      <DeleteModalHandler
        deleteModal={{ activeDeleteModal, setActiveDeleteModal }}
        isCloud={isCloud}
        index={index}
        deleteHandler={{ handleDeleteCloud, handleDeleteLocal }}
      />
    </>
  );
}
