interface ModalPropsType {
    children: React.ReactNode;
    setActiveModal: (active: boolean) => void;
}

export default function Modal({ children, setActiveModal }: ModalPropsType) {
    return (
        <div className="flex justify-center items-center fixed bg-snow-primary bg-opacity-[55%] h-full w-full top-0 left-0 z-10">
            <div className="relative overflow-auto h-[87%] w-11/12 rounded-lg bg-[#ECECEC] mx-2">
                {children}
                <button
                    onClick={() => setActiveModal(false)}
                    className='absolute left-2 top-2 material-symbols-rounded'
                >
                    close
                </button>
            </div>
        </div>
    );
}