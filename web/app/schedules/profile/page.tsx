'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

import useUser from '@/app/hooks/useUser';
import useClassesToShow from '@/app/hooks/useClassesToShow';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';

import LogoImage from '@/public/logo.png';
import defaultProfile from '@/public/profile.svg';

import Image from 'next/image';
import Button from '@/app/components/Button';
import Modal from '@/app/components/Modal/Modal';

import signInWithGoogle from '@/app/utils/signInWithGoogle';
import handleLogout from '@/app/utils/api/logout';
import useSchedules from '@/app/hooks/useSchedules';

export default function Profile() {
    const [activeModal, setActiveModal] = useState(false);

    const { setClassesToShow } = useClassesToShow();
    const { setSelectedClasses } = useSelectedClasses();
    const { localSchedules, setLocalSchedules } = useSchedules();

    const userContext = useUser();
    const { user } = userContext;
    const router = useRouter();

    function handleLogoutAndRedirect() {
        setClassesToShow(new Array());
        setSelectedClasses(new Map());
        setLocalSchedules(new Array(), false);
        handleLogout({ userContext, router });
    }

    return (
        <>
            {activeModal &&
                <Modal setActiveModal={setActiveModal} noExit>
                    <div className="flex flex-col items-center justify-center h-full gap-16">
                        <h1 className="font-semibold text-center">Vc tem grades não salvas na nuvem e vai perde-las!</h1>
                        <div>
                            <h2 className="font-semibold text-center">Tem certeza que quer sair?</h2>
                            <div className="flex gap-16 justify-center mt-4">
                                <Button onClick={() => setActiveModal(false)} className='bg-red-500'>
                                    Não
                                </Button>
                                <Button onClick={() => handleLogoutAndRedirect()} className='bg-primary'>
                                    Sim, eu quero!
                                </Button>
                            </div>
                        </div>
                    </div>
                </Modal>
            }
            <Image
                className='opacity-60 absolute inset-x-1/2 top-0 mt-[300px] ml-[-150px]'
                src={LogoImage}
                alt='Pessoa marcando datas em um calendário com borda azul'
                width={300} height={300}
            />
            <div className="w-[100px] h-[100px] absolute top-[60px] right-10 z-10">
                <Image
                    className='shadow-lg rounded-full border-[5px]'
                    src={user.picture_url || defaultProfile}
                    alt='Foto de perfil do usuário'
                    width={120} height={120}
                />
            </div>
            <div className="flex flex-col justify-end w-[131px] absolute h-36 bg-primary rounded-[15px] top-[140px] right-[25px] z-0">
                <Button onClick={() => signInWithGoogle(router)} className='!shadow-none'>
                    Trocar de conta
                </Button>
                <Button onClick={() => {
                    if (localSchedules.length) setActiveModal(true);
                    else handleLogoutAndRedirect();
                }} className='!shadow-none text-white'>
                    Sair
                </Button>
            </div>
        </>
    );
}