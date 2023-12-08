'use client';

import { useContext } from 'react';
import { ModalContext } from '../contexts/ModalContext';

export default function useModal() {
    const value = useContext(ModalContext);

    return value;
}