import { HTMLProps } from 'react';

interface ButtonPropsType extends HTMLProps<HTMLButtonElement> {
    children: React.ReactNode;
}

export default function Button({ children, ...props }: ButtonPropsType) {
    return (
        <button
            {...props}
            className={`flex justify-center items-center gap-3 font-medium rounded-xl shadow py-3 px-5 hover:shadow-md transition-all duration-300 ${props.className || ''}`}
            type='submit'
        >
            {children}
        </button>
    );
}