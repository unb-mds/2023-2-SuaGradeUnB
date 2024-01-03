import Image from 'next/image';

import closeIcon from '@/public/icons/close.jpg';

interface ModalPropsType {
    children: React.ReactNode;
    setActiveModal: (active: boolean) => void;
    noExit?: boolean;
}

export default function Modal({ children, setActiveModal, noExit }: ModalPropsType) {
    return (
        <div className="flex justify-center items-center fixed bg-snow-primary bg-opacity-[55%] h-full w-full top-0 left-0 z-50">
            <div className="relative overflow-auto h-[87%] w-11/12 rounded-lg bg-[#ECECEC] mx-2">
                {children}
                {!noExit &&
                    <button
                        onClick={() => setActiveModal(false)}
                        className='absolute left-2 top-2'
                    >
                        <Image
                            src={closeIcon}
                            alt="fechar"
                        />
                    </button>
                }
            </div>
        </div>
    );
}