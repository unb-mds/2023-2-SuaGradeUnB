'use client';
import Link from 'next/link';

import useUser from '@/app/hooks/useUser';

export default function Home() {
    const { user } = useUser();

    return (
    <main>
        <div className='flex flex-col justify-center items-center'>
        <Link href={''} className='flex flex-col items-center font-medium rounded w-2/4 py-2 px-1 shadow-2xl hover:shadow-md transition-all duration-300 bg-[#4080F4] text-white'>
        Adicionar materia</Link>
        </div>

    </main>
    );
}