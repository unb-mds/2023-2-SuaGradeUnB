import toast from 'react-hot-toast';

interface ToastOptions {
    duration?: number;
    centered?: boolean;
    style?: React.CSSProperties;
}

const createToast = (message: string, type: 'success' | 'error', options?: ToastOptions) => {
    const { duration = 5000, centered = true, style } = options || {};

    toast[type](message, {
        duration,
        style: {
            textAlign: centered ? 'center' : 'justify',
            ...style,
        },
    });
};

export const successToast = (message: string, options?: ToastOptions) => createToast(message, 'success', options);

export const errorToast = (message: string, options?: ToastOptions) => createToast(message, 'error', options);
