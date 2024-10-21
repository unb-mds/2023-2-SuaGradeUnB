'use client';

import { useRouter } from 'next/navigation';

import useUser from '@/app/hooks/useUser';
import useClassesToShow from '@/app/hooks/useClassesToShow';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';

import LogoImage from '@/public/logo.png';
import defaultProfile from '@/public/profile.svg';

import Image from 'next/image';
import Button from '@/app/components/Button';

import signInWithGoogle from '@/app/utils/signInWithGoogle';
import handleLogout from '@/app/utils/api/logout';
import useSchedules from '@/app/hooks/useSchedules';
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogTitle,
  DialogTrigger,
} from '@/app/components/ui/dialog';

export default function Profile() {
  const { setClassesToShow } = useClassesToShow();
  const { setSelectedClasses } = useSelectedClasses();
  const { localSchedules, setLocalSchedules, setCloudSchedules } =
    useSchedules();

  const userContext = useUser();
  const { user } = userContext;
  const router = useRouter();

  function handleLogoutAndRedirect() {
    setClassesToShow(new Array());
    setSelectedClasses(new Map());
    setLocalSchedules(new Array(), false);
    setCloudSchedules(new Array());
    handleLogout({ userContext, router });
  }

  return (
    <>
      <Image
        className="opacity-60 absolute inset-x-1/2 top-0 mt-[300px] ml-[-150px]"
        src={LogoImage}
        alt="Pessoa marcando datas em um calendário com borda azul"
        width={300}
        height={300}
      />

      <div className="w-[100px] h-[100px] absolute top-[60px] right-10 z-10">
        <Image
          className="shadow-lg rounded-full border-[5px]"
          src={user.picture_url || defaultProfile}
          alt="Foto de perfil do usuário"
          width={120}
          height={120}
        />
      </div>
      <div className="flex flex-col justify-end w-[131px] absolute h-36 bg-primary rounded-[15px] top-[140px] right-[25px] z-0">
        <Button
          onClick={() => signInWithGoogle(router)}
          className="!shadow-none"
        >
          Trocar de conta
        </Button>

        {localSchedules.length > 0 ? (
          <Dialog>
            <DialogTrigger asChild>
              <Button className="!shadow-none text-white">Sair</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogTitle>Tem certeza que quer sair?</DialogTitle>
              <div className="flex flex-col items-center justify-center gap-4 w-full">
                <h1 className="font-semibold text-center">
                  Você tem grades não salvas na nuvem e vai perdê-las!
                </h1>

                <div>
                  <div className="flex items-center gap-4 justify-between w-full">
                    <DialogClose>
                      <Button className="bg-red-500 text-sm" aria-label="Cancelar">
                        Cancelar
                      </Button>
                    </DialogClose>
                    <DialogClose>
                      <Button
                        onClick={() => handleLogoutAndRedirect()}
                        className="bg-primary text-sm"
                        aria-label="Sair mesmo assim"
                      >
                        Sair mesmo assim
                      </Button>
                    </DialogClose>
                  </div>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        ) : (
          <Button
            onClick={() => handleLogoutAndRedirect()}
            className="!shadow-none text-white"
          >
            Sair
          </Button>
        )}
      </div>
    </>
  );
}
