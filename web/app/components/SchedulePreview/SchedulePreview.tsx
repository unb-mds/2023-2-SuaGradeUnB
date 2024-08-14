'use client';

import React from 'react';
import useSchedules from '@/app/hooks/useSchedules';
import useUser from '@/app/hooks/useUser';

import { ScheduleClassType } from '@/app/contexts/SchedulesContext';

import Modal from '../Modal/Modal';
import Schedule from '../Schedule/Schedule';
import Button from '../Button';

import saveSchedule from '@/app/utils/api/saveSchedule';
import getSchedules from '@/app/utils/api/getSchedules';
import deleteSchedule from '@/app/utils/api/deleteSchedule';
import { errorToast, successToast } from '@/app/utils/toast';

import jsPDF from 'jspdf';
import { AxiosError } from 'axios';
import { FiDownload, FiTrash2, FiUploadCloud } from 'react-icons/fi';
import { Tooltip, TooltipContent, TooltipTrigger } from '../ui/tooltip';
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogTitle,
  DialogTrigger,
} from '../ui/dialog';
import { moment } from '@/app/utils/moment';

interface GenericSchedule {
  id?: number;
  created_at: string;
  classes: Array<ScheduleClassType>;
  type: 'local' | 'cloud';
}

export default function SchedulePreview({
  schedule,
  index,
  position,
}: {
  schedule: GenericSchedule;
  index: number;
  position: number;
}) {
  const { user } = useUser();
  const { localSchedules, setCloudSchedules, setLocalSchedules } =
    useSchedules();

  const isCloud = schedule.type === 'cloud';

  const scheduleId = `download-content-${position}-${
    isCloud ? 'cloud' : 'local'
  }`;

  async function handleDeleteCloud() {
    const response = await deleteSchedule(schedule?.id, user.access);

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

  async function handleDelete() {
    if (isCloud) await handleDeleteCloud();
    else handleDeleteLocal();
  }

  return (
    <>
      <div className="relative w-full max-w-sm">
        <div className="hidden">
          <Schedule
            id={scheduleId}
            schedules={schedule.classes}
            toDownload={true}
          />
        </div>
        <Dialog>
          <DialogTrigger asChild>
            <div className="flex justify-center items-center bg-snow-tertiary h-48 rounded-3xl">
              <Schedule schedules={schedule.classes} preview />
            </div>
          </DialogTrigger>
          <DialogContent className="overflow-auto max-w-screen-xl ">
            <Schedule schedules={schedule.classes} />
          </DialogContent>
        </Dialog>
        <ActionButtons
          schedule={schedule}
          position={position}
          handleDelete={handleDelete}
        />
      </div>
    </>
  );
}

function ActionButtons({
  schedule,
  handleDelete,
  position,
}: {
  schedule: GenericSchedule;
  handleDelete: () => Promise<void>;
  position: number;
}) {
  const { user } = useUser();
  const isCloud = schedule.type === 'cloud';

  return (
    <div
      className={`flex justify-between items-center w-full ${
        isCloud ? '-bottom-14' : '-bottom-7'
      }`}
    >
      <div className="mt-3">
        <p className="text-black opacity-40 text-lg font-bold">
          Grade {position}
        </p>
        {isCloud && schedule.created_at && (
          <p className="text-sm font-normal opacity-40">
            {moment(schedule.created_at).format('dddd, DD [de] MMMM, YYYY')}
          </p>
        )}
      </div>
      <div className="flex gap-4 h-[25px]">
        {!isCloud && !user.is_anonymous && (
          <UploadToCloudButton
            schedules={{
              localSchedule: schedule.classes,
            }}
            handleDelete={handleDelete}
          />
        )}
        <Tooltip>
          <TooltipTrigger asChild>
            <button
              onClick={() => {
                handleDownloadPDF(isCloud, position);
              }}
            >
              <FiDownload size={24} className="opacity-50" />
            </button>
          </TooltipTrigger>
          <TooltipContent sideOffset={5} align="center">
            Baixar
          </TooltipContent>
        </Tooltip>
        <Dialog>
          <DialogTrigger>
            <Tooltip>
              <TooltipTrigger asChild>
                <button>
                  <FiTrash2 size={24} className="opacity-50" />
                </button>
              </TooltipTrigger>
              <TooltipContent sideOffset={5} align="center">
                Deletar
              </TooltipContent>
            </Tooltip>
          </DialogTrigger>
          <DialogContent>
            <DialogTitle>Deletar grade</DialogTitle>
            <div className="flex flex-col gap-4 mt-4">
              <h1 className="font-semibold text-center">
                A grade será deletada para sempre, tem certeza?
              </h1>
              <DialogFooter>
                <div className="flex  w-full gap-2 items-center">
                  <DialogClose asChild>
                    <Button className="bg-gray-400 flex-1">Não</Button>
                  </DialogClose>
                  <DialogClose asChild>
                    <Button
                      onClick={() => handleDelete()}
                      className="bg-primary flex-1"
                    >
                      Sim
                    </Button>
                  </DialogClose>
                </div>
              </DialogFooter>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
}

const commonError = () =>
  errorToast('Houve um erro na atualização das grades!');

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

  async function handleUploadToCloud() {
    saveSchedule(props.schedules.localSchedule, user.access)
      .then((response) => {
        if (response.status == 201) handleSuccessToSave();
      })
      .catch((error: any) => handleErrorToSave(error));
  }

  return (
    <Tooltip>
      <TooltipTrigger asChild>
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
  const doc = document.getElementById(
    `download-content-${index}-${isCloud ? 'cloud' : 'local'}`
  );
  console.log(doc, `download-content-${index}-${isCloud ? 'cloud' : 'local'}`);

  if (!doc) return;

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
