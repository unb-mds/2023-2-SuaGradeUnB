import toast from 'react-hot-toast';

export const errorToast = (message: string) => {
    toast.error(message, {
        style: {
            textAlign: 'center'
        }
    });
};