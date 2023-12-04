import { MutableRefObject } from 'react';

import Button from '@/app/components/Button';
import useShowPopUpContent from '@/app/hooks/useShowPopUpContent';
import useWindowDimensions from '@/app/hooks/useWindowDimensions';

interface AddDisciplineButtonPropsType {
    buttonAddDisciplineRef: MutableRefObject<HTMLButtonElement | null>;
}

export default function AddDisciplineButton(props: AddDisciplineButtonPropsType) {
    const { breakHeighPoint } = useWindowDimensions();
    const { showPopUpContent, setShowPopUpContent } = useShowPopUpContent();

    return (
        <div className='flex justify-center'>
            <Button
                innerRef={props.buttonAddDisciplineRef}
                onClick={() => setShowPopUpContent(!showPopUpContent)}
                className={`absolute ${breakHeighPoint ? 'top-20' : 'top-3'} font-semibold bg-secondary`}
            >
                Buscar matéria
            </Button>
        </div>
    );
}