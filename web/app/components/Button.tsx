import { HTMLProps, LegacyRef } from 'react';
import { twMerge } from 'tailwind-merge';

interface ButtonPropsType extends HTMLProps<HTMLButtonElement> {
  children: React.ReactNode;
  innerRef?: LegacyRef<HTMLButtonElement> | undefined;
}

export default function Button({
  children,
  innerRef,
  ...props
}: ButtonPropsType) {
  return (
    <button
      ref={innerRef}
      {...props}
      className={twMerge(
        'flex justify-center items-center gap-3 font-medium rounded-xl shadow py-3 px-5 hover:shadow-md transition-all duration-300 text-white',
        props.className
      )}
      type="submit"
    >
      {children}
    </button>
  );
}
