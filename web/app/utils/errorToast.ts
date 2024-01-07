import toast from 'react-hot-toast';
import React from 'react';

export const errorToast = (message: string, centered: boolean = true) => {
    toast.error(message, {
        duration: 5000,
        style: {
            textAlign: centered ? 'center' : 'justify'
        },
    });
};