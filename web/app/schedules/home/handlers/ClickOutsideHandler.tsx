'use client';

import { useEffect } from 'react';

import useShowPopUpContent from '@/app/hooks/useShowPopUpContent';

interface ClickOutsideHandlerPropsType {
    children: React.ReactNode;
    refs: {
        divAddClassRef: React.MutableRefObject<HTMLDivElement | null>;
        buttonAddDisciplineRef: React.MutableRefObject<HTMLButtonElement | null>;
    }
}

export default function ClickOutsideHandler({ children, ...props }: ClickOutsideHandlerPropsType) {
    const { setShowPopUpContent } = useShowPopUpContent();
    const { divAddClassRef, buttonAddDisciplineRef } = props.refs;

    useEffect(() => {
        const handleClickOutside = (event: Event) => {
            const element: Node = event.target as Node;

            if (divAddClassRef.current && buttonAddDisciplineRef.current) {
                const checkButtonAddDiscipline: boolean = buttonAddDisciplineRef.current == element;
                const checkDivAddClass: boolean = (divAddClassRef.current as HTMLElement).contains(element);

                if (!checkButtonAddDiscipline && !checkDivAddClass) setShowPopUpContent(false);
            }
        };
        document.addEventListener('click', handleClickOutside);

        return () => document.removeEventListener('click', handleClickOutside);
    }, [buttonAddDisciplineRef, divAddClassRef, setShowPopUpContent]);

    return children;
}