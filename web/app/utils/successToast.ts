import toast from 'react-hot-toast';
import React from 'react';

export const successToast = (message: string, centered: boolean = true) => {
    toast.success(message, {
        duration: 5000,
        style: {
            textAlign: centered ? 'center' : 'justify'
        },
    });
};
