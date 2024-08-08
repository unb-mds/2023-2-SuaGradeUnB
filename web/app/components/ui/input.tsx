import * as React from 'react';
import { cn } from '@/app/utils/utils';

const InputRoot = ({
  children,
}: {
  children: JSX.Element | JSX.Element[];
}): JSX.Element => {
  return (
    <div className="flex justify-center bg-white shadow-md rounded-full">
      {children}
    </div>
  );
};

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => {
    return (
      <InputRoot>
        <input
          ref={ref}
          className={cn(
            'w-full p-2 rounded-full bg-transparent focus:outline-none focus-within:',
            className
          )}
          {...props}
        />
      </InputRoot>
    );
  }
);

Input.displayName = 'Input';
