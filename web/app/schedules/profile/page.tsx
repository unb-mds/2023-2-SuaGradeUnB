'use client';

import Image from 'next/image';
import { useRouter } from 'next/navigation';

import useUser from '@/app/hooks/useUser';

import LogoImage from '@/public/logo.svg';
import defaultProfile from '@/public/profile.svg';

import Button from '@/app/components/Button';

import signInWithGoogle from '@/app/utils/signInWithGoogle';

export default function Profile() {
    const { user } = useUser();
    const router = useRouter();

    return (
        <>
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
                <Button className='!shadow-none'>
                    Sair
                </Button>
            </div>
        </>

    );
}