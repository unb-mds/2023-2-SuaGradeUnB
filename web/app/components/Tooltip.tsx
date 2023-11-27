'use client';

import styles from '@/app/styles/tooltip.module.css';

import useWindowDimensions from '../hooks/useWindowDimensions';
import { useState } from 'react';

interface TooltipPropsType {
    children: React.ReactNode,
};

export default function Tooltip({ children }: TooltipPropsType) {
    const [active, setActive] = useState(false);
    const { width } = useWindowDimensions();

    const isMobile = () => {
        return width && width <= 768;
    };

    return (
        <div className={styles.tooltip}>
            <span
                onClick={() => setActive(true)}
                className='flex justify-center items-center material-symbols-rounded text-xs border-black border-solid border-2 rounded-full h-5 w-5 hover:bg-gray-300'>
                question_mark
            </span>
            <span className={`${active ? 'visible' : 'invisible'} ${styles.inside} ${styles.tooltiptext} p-2`}>
                <div className='relative flex flex-col gap-1 justify-center items-center w-4/5 rounded-md p-5 bg-snow-primary'>
                    {children}
                    <button
                        onClick={() => setActive(false)}
                        className={`absolute right-2 ${isMobile() ? 'bottom-2' : 'top-2'} material-symbols-rounded`}
                    >
                        close
                    </button>
                </div>
            </span>
        </div>
    );
}