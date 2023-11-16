'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import useUser from '../hooks/useUser';

import signInWithGoogle from '../utils/signInWithGoogle';
import registerWithGoogle from '../utils/api/registerWithGoogle';
import retrieveAccessToken from '../utils/retrieveAccessToken';

import googleLogoImage from '../../public/google.svg';

import Image from 'next/image';
import Button from './Button';
import toast from 'react-hot-toast';

export interface UserData {
    access: string;
    first_name: string;
    email: string;
    picture_url: string;
}

export default function SignInSection() {
    const router = useRouter();
    const { user, setUser } = useUser();
    const [accessToken, setAccessToken] = useState<string>();

    useEffect(() => {
        setAccessToken(retrieveAccessToken());
    }, [setAccessToken]);

    useEffect(() => {
        if (accessToken) {
            registerWithGoogle(accessToken).then(response => {
                const userData: UserData = response.data;
                setUser({
                    is_anonymous: false,
                    access: userData.access,
                    first_name: userData.first_name,
                    email: userData.email,
                    picture_url: userData.picture_url
                });
                router.push('/schedules/home');
            }).catch(error => {
                toast.error('Algo deu errado: ' + error.response.data.errors);
            });
        }
    }, [accessToken, router, setUser]);

    return (
        <Button
            className='text-sm hover:bg-slate-100 bg-white text-black'
            onClick={() => {
                if (!user.is_anonymous) router.push('/schedules/home');
                else signInWithGoogle(router);
            }}
        >
            <Image
                src={googleLogoImage} alt='Logo do Google'
            />
            Continuar com o Google
        </Button>

    );
}