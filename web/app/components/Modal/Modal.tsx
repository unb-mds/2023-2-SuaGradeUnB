import useModal from '@/app/hooks/useModal';
import useWindowDimensions from '@/app/hooks/useWindowDimensions';

import { isMobile } from '../AsideSchedulePopUp/Tooltip';

interface ModalPropsType {
    children: React.ReactNode;
}

export default function Modal({ children }: ModalPropsType) {
    const { width } = useWindowDimensions();
    const { setActiveModel } = useModal();

    return (
        <div className="flex justify-center items-center fixed bg-snow-primary bg-opacity-[55%] h-full w-full top-0 left-0 z-10">
            <div className="relative overflow-x-auto flex flex-col gap-1 justify-center items-start rounded-md p-5 pb-8 bg-blue-500 mx-2">
                {children}
                <button
                    onClick={() => setActiveModel(false)}
                    className={`absolute left-2 ${isMobile(width) ? 'bottom-2' : 'top-2'} material-symbols-rounded`}
                >
                    close
                </button>
            </div>
        </div>
    );
}