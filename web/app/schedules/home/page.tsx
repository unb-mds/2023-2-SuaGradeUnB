'use client';
import Link from 'next/link';

import { useEffect, useState } from 'react';
import useUser from '@/app/hooks/useUser';
import Button from '@/app/components/Button';

import DisciplineBox from '@/app/components/DisciplineBox';

export default function Home() {
   const { user } = useUser();
   const [showContent, setShowContent] = useState(false);
   useEffect(() => {
      const handleClickOutside = (event: Event) => {
         const divAddClass = document.getElementById('addClass');
         const divAddDiscipline = document.getElementById('addDiscipline');
         if (divAddClass && divAddDiscipline && !divAddDiscipline.contains(event.target as Node) && !divAddClass.contains(event.target as Node)) {
            setShowContent(false);
         }
      };
      document.addEventListener('click', handleClickOutside);

      return () => {
         document.removeEventListener('click', handleClickOutside);
      };
   }, []);

   return (
      <>
         <div className='flex flex-col justify-center items-center'>
            <Link href={''} onClick={() => {
               setShowContent(!showContent);
            }} id='addDiscipline' className='flex flex-col absolute top-24 items-center font-semibold rounded-lg py-2 px-4 shadow-md hover:shadow-md transition-all duration-300 bg-[#4080F4] text-white tracking-tighter'>
               Adicionar matéria
            </Link>
         </div>

         <div className='flex flex-col items-center gap-5 overflow-auto h-3/5 pt-5 pb-2'>
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
         </div>

         <div className='flex justify-center z-10'>
            <div id='addClass' className={`w-11/12 ${showContent ? 'h-5/6' : 'h-0'} hide transition-all duration-500 m-auto absolute bottom-0 flex justify-center items-center rounded-t-[40px] bg-slate-200/100 z-10 ${user}`}>
               {showContent && ( 
                  <button className = 'relative inset-x-0 -bottom-80 shadow-lg justify-center items-center gap-3 font-medium rounded-xl py-3 px-5 hover:shadow-md bg-primary text-white'>
                     Adicionar
                  </button>
               )}

            </div>
         </div>

         <div className='flex flex-col justify-center items-center z-0'>
            <Link href={''} className='flex justify-center absolute bottom-32 items-center rounded-xl w-52 h-10 bg-primary text-white font-semibold'>
               Gerar Grade
            </Link>
         </div>
      </>
   );
}