'use client';

import useUser from '../hooks/useUser';

export default function Schedule() {
    const { user } = useUser();

    return (
        <main className='flex flex-col justify-center items-center gap-8 text-white mt-16 p-8'>
            <h1 className='text-xl font-bold'>
                {user.is_anonymous ? 'Bem vindo, você está como anônimo' : `Bem vindo, ${user?.first_name}`}
            </h1>
            <p>{user?.email}</p>
        </main>
    );
}