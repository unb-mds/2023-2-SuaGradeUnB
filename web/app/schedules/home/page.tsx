'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';

import Button from '@/app/components/Button';
import DisciplineBox from '@/app/components/DisciplineBox';
import AsideSchedulePopUp from '@/app/components/AsideSchedulePopUp';

export default function Home() {
   const router = useRouter();

   const [showContent, setShowContent] = useState(false);

   const divAddClassRef = useRef(null);
   const buttonAddDisciplineRef = useRef(null);

   useEffect(() => {
      const handleClickOutside = (event: Event) => {
         const element: Node = event.target as Node;

         if (divAddClassRef.current && buttonAddDisciplineRef.current) {
            const checkButtonAddDiscipline: boolean = buttonAddDisciplineRef.current == element;
            const checkDivAddClass: boolean = (divAddClassRef.current as HTMLElement).contains(element);

            if (!checkButtonAddDiscipline && !checkDivAddClass) setShowContent(false);
         }
      };
      document.addEventListener('click', handleClickOutside);

      return () => {
         document.removeEventListener('click', handleClickOutside);
      };
   }, []);

   return (
      <>
         <div className='flex justify-center'>
            <Button
               innerRef={buttonAddDisciplineRef}
               onClick={() => setShowContent(!showContent)}
               className='absolute top-24 font-semibold bg-secondary'
            >
               Adicionar matéria
            </Button>
         </div>

         <div className='flex flex-col items-center gap-5 overflow-auto max-h-full pb-2'>
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
            <DisciplineBox name='Cálculo 1' code='MAT0025' teachers={['Ricardo', 'dois', 'três']} schedule='Segunda, Terça - Tal Horário' />
         </div>

         <AsideSchedulePopUp content={{ showContent, setShowContent }} divAddClassRef={divAddClassRef} />

         <div className='flex justify-center'>
            <Button
               onClick={() => router.replace('/schedules/mygrades')}
               className='absolute bottom-32 w-52 h-10 font-semibold bg-primary'
            >
               Gerar Grade
            </Button>
         </div>
      </>
   );
}