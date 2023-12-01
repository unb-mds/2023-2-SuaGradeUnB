'use client';

import { useContext } from 'react';
import { ClassesToShowContext } from '../contexts/ClassesToShowContext';

export default function useClassesToShow() {
    const value = useContext(ClassesToShowContext);

    return value;
}