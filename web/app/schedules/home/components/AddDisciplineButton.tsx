import { MutableRefObject } from 'react';

import Button from '@/app/components/Button';
import useShowPopUpContent from '@/app/hooks/useShowPopUpContent';

interface AddDisciplineButtonPropsType {
    buttonAddDisciplineRef: MutableRefObject<HTMLButtonElement | null>;
}

export default function AddDisciplineButton(props: AddDisciplineButtonPropsType) {
    const { showPopUpContent, setShowPopUpContent } = useShowPopUpContent();

    return (
        <div className='flex justify-center'>
            <Button
                innerRef={props.buttonAddDisciplineRef}
                onClick={() => setShowPopUpContent(!showPopUpContent)}
                className='absolute top-20 font-semibold bg-secondary'
            >
                Adicionar matéria
            </Button>
        </div>
    );
}