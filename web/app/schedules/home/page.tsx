'use client';
import Link from 'next/link';

import useUser from '@/app/hooks/useUser';

export default function Home() {
    const { user } = useUser();

    return (
    <main> 

        <div className='flex flex-col justify-center items-center'>
          <Link href={''} className='flex flex-col items-center font-semibold rounded-lg py-2 px-4 mb-6 shadow-md hover:shadow-md transition-all duration-300 bg-[#4080F4] text-white tracking-tighter'>
            Adicionar matéria
          </Link>
        </div>
        
        <div className='flex flex-col justify-center items-center gap-5'>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data
         </span>
        </div>

        <div className='flex flex-col justify-center items-center mt-12'>
           <Link href={''} className='flex justify-center items-center rounded-xl w-52 h-10 bg-primary text-white font-semibold '>
            Gerar Grade
           </Link> 
        </div>

    </main>
    );
}