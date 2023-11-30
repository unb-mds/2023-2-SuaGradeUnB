import { createContext, useState } from 'react';

interface ShowPopUpContentContextType {
    showPopUpContent: boolean;
    setShowPopUpContent: React.Dispatch<React.SetStateAction<boolean>>;
}

interface ShowPopUpContentContextProviderPropsType {
    children: React.ReactNode;
}

export const ShowPopUpContentContext = createContext({} as ShowPopUpContentContextType);

export default function ShowPopUpContentContextProvider({ children, ...props }: ShowPopUpContentContextProviderPropsType) {
    const [showPopUpContent, setShowPopUpContent] = useState(false);

    return (
        <ShowPopUpContentContext.Provider value={{ showPopUpContent, setShowPopUpContent }}>
            {children}
        </ShowPopUpContentContext.Provider>
    );
}