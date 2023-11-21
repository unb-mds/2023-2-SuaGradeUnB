'use client';
import Link from 'next/link';

import useUser from '@/app/hooks/useUser';

export default function Home() {
    const { user } = useUser();

    return (
    <>
      <div className='flex flex-col justify-center items-center'>
          <Link href={''} className='flex flex-col absolute top-24 items-center font-semibold rounded-lg py-2 px-4 shadow-md hover:shadow-md transition-all duration-300 bg-[#4080F4] text-white tracking-tighter'>
            Adicionar matéria
          </Link>
      </div>

        <div className='flex flex-col justify-center items-center gap-5 overflow-auto h-3/5 pt-72 pb-2'>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data first
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
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data last
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data last
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data last
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data last
         </span>
         <span className='flex flex-row items-center rounded-lg font-semibold w-10/12 h-10 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            data last
         </span>
        </div>

      <div className='flex flex-col justify-center items-center'>
        <Link href={''} className='flex justify-center absolute bottom-32 items-center rounded-xl w-52 h-10 bg-primary text-white font-semibold '>
         Gerar Grade
        </Link> 
      </div>
   </>
    );
}