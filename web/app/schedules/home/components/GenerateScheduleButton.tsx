'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import useClassesToShow from '@/app/hooks/useClassesToShow';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';
import useSchedules from '@/app/hooks/useSchedules';
import useUser from '@/app/hooks/useUser';

import Button from '@/app/components/Button';

import {
  ScheduleAPIType,
  ScheduleClassType,
} from '@/app/contexts/SchedulesContext';

import generateSchedule, {
  EachFieldNumber,
} from '@/app/utils/api/generateSchedule';
import { errorToast } from '@/app/utils/toast';
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogTitle,
  DialogTrigger,
} from '@/app/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/app/components/ui/select';

function PreferenceOrder({
  setPreference,
}: {
  setPreference: (preference: EachFieldNumber) => void;
}) {
  return (
    <Select
      onValueChange={(value) => {
        const preference = parseInt(value) as EachFieldNumber;
        setPreference(preference);
      }}
      defaultValue="1"
    >
      <SelectTrigger className="bg-white shadow-md h-14 p-2 rounded-xl">
        <SelectValue></SelectValue>
      </SelectTrigger>

      <SelectContent>
        <SelectItem value="1">Mínima</SelectItem>
        <SelectItem value="2">Média</SelectItem>
        <SelectItem value="3">Máxima</SelectItem>
      </SelectContent>
    </Select>
  );
}

export default function GenerateScheduleButton() {
  const router = useRouter();

  const { setLoading } = useUser();
  const { setLocalSchedules } = useSchedules();
  const { selectedClasses } = useSelectedClasses();
  const { classesToShow } = useClassesToShow();

  const [morningPreference, setMorningPreference] =
    useState<EachFieldNumber>(1);
  const [afternoonPreference, setAfternoonPreference] =
    useState<EachFieldNumber>(1);
  const [nightPreference, setNightPreference] = useState<EachFieldNumber>(1);

  const createSchedule = () => {
    let classes_id = new Array();
    selectedClasses.forEach((_class) => {
      Array.from(_class.keys()).forEach((key) => {
        classes_id.push(key);
      });
    });

    setLoading(true);
    generateSchedule(classes_id, [
      morningPreference,
      afternoonPreference,
      nightPreference,
    ]).then((response) => {
      if (response.status === 200) {
        const data = response.data as ScheduleAPIType;
        const schedules = data.schedules as Array<ScheduleClassType>;

        if (!schedules.length) {
          errorToast(data.message, {
            centered: data.message.split('\n').length == 1,
          });
          setLoading(false);
        } else {
          setLocalSchedules(schedules);
          router.replace('/schedules/mygrades');
          setTimeout(() => {
            setLoading(false);
          }, 500);
        }
      } else {
        errorToast(
          'Não foi possível gerar as grades, tente novamente mais tarde!'
        );
        setLoading(false);
      }
    });
  };

  return (
    <>
      <Dialog>
        <DialogTrigger asChild>
          <div className="flex justify-center w-[100vw]">
            <Button
              disabled={!classesToShow.length}
              className="fixed bottom-20 w-52 h-10 font-semibold cursor-pointer bg-primary disabled:opacity-70 disabled:cursor-not-allowed"
            >
              Gerar Grade
            </Button>
          </div>
        </DialogTrigger>

        <DialogContent className="max-w-lg bg-snow-secondary">
          <DialogTitle>Período de preferência</DialogTitle>

          <div className="flex flex-col justify-center items-center gap-10 p-3 h-full">
            <div className="flex flex-col gap-3">
              <div className="grid grid-cols-3 gap-3 font-medium text-center">
                <span>Manhã</span>
                <span>Tarde</span>
                <span>Noite</span>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <PreferenceOrder setPreference={setMorningPreference} />
                <PreferenceOrder setPreference={setAfternoonPreference} />
                <PreferenceOrder setPreference={setNightPreference} />
              </div>
            </div>
          </div>

          <DialogFooter>
            <div className="flex justify-between items-center w-full">
              <DialogClose asChild>
                <Button className="bg-gray-400">Cancelar</Button>
              </DialogClose>
              <Button className="bg-primary" onClick={createSchedule}>
                Gerar
              </Button>
            </div>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
