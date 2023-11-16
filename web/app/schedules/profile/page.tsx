'use client';

import useUser from '@/app/hooks/useUser';
import Image from 'next/image';
import LogoImage from '@/public/logo.svg';
import Button from '@/app/components/Button';
import signInWithGoogle from '@/app/utils/signInWithGoogle';
import { useRouter } from 'next/navigation';
import defaultProfile from '@/public/profile.svg';

export default function Profile() {
    const router = useRouter();
    const { user } = useUser();
    

    function handleSignOut() {

    }

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
                    className='rounded-full border-[5px]'
                    src={defaultProfile}
                    alt='Foto de perfil do usuário'
                    width={120} height={120}
                />
            </div>

            <div className="flex flex-col justify-end w-[131px] absolute h-36 bg-primary rounded-[15px] top-[140px] right-[25px] z-0">
                <Button onClick={() => signInWithGoogle(router)} className='!shadow-none text-white'>
                    Trocar de conta
                </Button>
                <Button className='!shadow-none text-white'>
                    Sair
                </Button>
            </div>
        </>

    );
}