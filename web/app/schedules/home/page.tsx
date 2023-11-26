'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import useSelectedClasses from '@/app/hooks/useSelectedClasses';

import { ClassValueType } from '@/app/contexts/SelectedClassesContext';

import Button from '@/app/components/Button';
import DisciplineBox from '@/app/components/DisciplineBox';
import AsideSchedulePopUp from '@/app/components/AsideSchedulePopUp/AsideSchedulePopUp';

export default function Home() {
   const router = useRouter();

   const [classesToShow, setClassesToShow] = useState<Array<ClassValueType>>([]);
   const { classesChange, selectedClasses } = useSelectedClasses();
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

   useEffect(() => {
      const newClasses = new Array();
      selectedClasses.forEach((cls) => {
         cls.forEach(value => {
            newClasses.push(value);
         });
      });
      setClassesToShow(newClasses);
   }, [classesChange, selectedClasses]);

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

         <div className={`flex flex-col items-center ${classesToShow.length ? '' : 'justify-center'} gap-5 overflow-auto min-h-full max-h-full pb-2`}>
            {classesToShow.length ? classesToShow.map((cls, index) =>
               <DisciplineBox
                  key={index}
                  currentClass={cls} discipline={cls.discipline}
               />
            ) : 'Nenhuma disciplina escolhida no momento'}
         </div>

         <AsideSchedulePopUp content={{ showContent, setShowContent }} divAddClassRef={divAddClassRef} />

         <div className='flex justify-center'>
            <Button
               disabled={classesToShow.length === 0}
               onClick={() => router.replace('/schedules/mygrades')}
               className='absolute bottom-28 w-52 h-10 font-semibold bg-primary disabled:opacity-70'
            >
               Gerar Grade
            </Button>
         </div>
      </>
   );
}