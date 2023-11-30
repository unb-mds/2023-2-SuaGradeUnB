'use client';

import { useContext } from 'react';
import { ShowPopUpContentContext } from '../contexts/ShowPopUpContentContext';

export default function useShowPopUpContent() {
    const value = useContext(ShowPopUpContentContext);

    return value;
}