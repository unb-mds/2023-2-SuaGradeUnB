import Image, { StaticImageData } from 'next/image';

import Button from './Button';

interface AsideButtonPropsType {
    image: StaticImageData;
    text: string;
    onClick?: () => void;
}


export default function AsideButton({ image, text, onClick }: AsideButtonPropsType) {
    return (
        <Button onClick={onClick} className='z-10 flex-col w-full !pb-0 !gap-1 !shadow-none !text-black'>
            <Image
                width={25} height={25}
                src={image} alt={`ícone da página ${text}`}
            />
            <span>
                {text}
            </span>
        </Button>
    );
}