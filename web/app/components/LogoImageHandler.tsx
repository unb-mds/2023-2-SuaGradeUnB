'use client';

import Image from 'next/image';

import logoImage from '../../public/logo.png';

import useWindowDimensions from '../hooks/useWindowDimensions';

const MIN_HEIGHT = 720;

export default function LogoImageHandler() {
    const { height } = useWindowDimensions();

    if (height && height <= MIN_HEIGHT) return null;

    return (
        <Image
            src={logoImage}
            alt='Pessoa marcando datas em um calendário com borda azul'
        />
    );
}