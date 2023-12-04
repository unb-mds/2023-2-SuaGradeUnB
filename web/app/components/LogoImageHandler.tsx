'use client';

import Image from 'next/image';

import logoImage from '../../public/logo.png';

import useWindowDimensions from '../hooks/useWindowDimensions';

export default function LogoImageHandler() {
    const { height } = useWindowDimensions();

    if (height && height <= 675) return null;

    return (
        <Image
            src={logoImage}
            alt='Pessoa marcando datas em um calendário com borda azul'
        />
    );
}