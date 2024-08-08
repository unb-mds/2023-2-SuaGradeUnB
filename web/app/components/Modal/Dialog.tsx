"use client";

import React, { createContext, useState } from "react";

interface ModalContextType {
  activeModal: boolean;
  setActiveModal: (value: boolean) => void;
}

const ModalContext = createContext<ModalContextType>({
  activeModal: false,
  setActiveModal: (value: boolean) => {},
});

const ModalProvider = ({ children }) => {
  const [activeModal, setActiveModal] = useState(false);

  return (
    <ModalContext.Provider value={{ activeModal, setActiveModal }}>
      {children}
    </ModalContext.Provider>
  );
};

const DialogContent = React.forwardRef<HTMLDivElement, { children: React.ReactNode; noExit?: boolean; setActiveModal: (value: boolean) => void }>(
  {
    children,
    noExit,
    setActiveModal,
  }
) => {
  return (
    <div className="flex justify-center items-center fixed bg-snow-primary bg-opacity-[55%] h-full w-full top-0 left-0 z-50">
      <div className="relative overflow-auto h-[87%] w-11/12 rounded-lg bg-[#ECECEC] mx-2">
        {children}
        {!noExit && (
          <button onClick={() => setActiveModal(false)} className="absolute left-2 top-2">
            <Image src={closeIcon} alt="fechar" />
          </button>
        )}
      </div>
    </div>
  );
};

export { ModalProvider, ModalContext };
