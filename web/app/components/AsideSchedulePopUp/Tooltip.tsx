'use client';

import styles from '@/app/styles/tooltip.module.css';

import Image from 'next/image';

import useWindowDimensions from '../../hooks/useWindowDimensions';
import { useEffect, useState } from 'react';

import questionIcon from '@/public/icons/question.jpg';
import closeIcon from '@/public/icons/close.jpg';

interface TooltipPropsType {
  children: React.ReactNode;
}

export const isMobile = (width?: number) => {
  return width && width <= 768;
};

export default function Tooltip({ children }: TooltipPropsType) {
  const [active, setActive] = useState(false);
  const { width } = useWindowDimensions();

  useEffect(() => {
    function keyPress(event: KeyboardEvent) {
      if (event.key === 'Escape') setActive(false);
    }

    if (active) document.addEventListener('keydown', keyPress);

    return () => {
      document.removeEventListener('keydown', keyPress);
    };
  }, [active]);

  return (
    <div className={styles.tooltip}>
      <span
        onClick={() => setActive(!active)}
        className="flex justify-center items-center text-xs border-black border-solid border-2 rounded-full h-5 w-5 hover:bg-gray-300"
      >
        <Image
          width={15}
          height={15}
          src={questionIcon}
          alt="ícone de interrogação"
        />
      </span>
      <span
        className={`${active ? 'visible' : 'invisible'} ${styles.inside} ${
          styles.tooltiptext
        } p-2`}
      >
        <div className="relative flex flex-col gap-1 justify-center items-center rounded-md p-5 bg-snow-primary">
          {children}
          <button
            onClick={() => setActive(false)}
            className={`absolute right-2 ${
              isMobile(width) ? 'bottom-2' : 'top-2'
            }`}
          >
            <Image src={closeIcon} alt="fechar" />
          </button>
        </div>
      </span>
    </div>
  );
}
