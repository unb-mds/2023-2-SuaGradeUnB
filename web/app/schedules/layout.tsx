'use client';

import { usePathname, useRouter } from 'next/navigation';
import useUser from '@/app/hooks/useUser';
import { useCallback, useState } from 'react';
import Button from '../components/Button';
import Image from 'next/image';

import AsideButton from '../components/AsideButton';
import Protected from '../components/Protected';
import { LoadingScreen } from '../components/LoadingScreen';
import InfoHeader from '../components/InfoHeader';

import homeIcon from '@/public/icons/home.jpg';
import infoIcon from '@/public/icons/info.jpg';
import logoIcon from '@/public/icons/logotipo.jpg';
import scheduleIcon from '@/public/icons/schedule.jpg';
import profileIcon from '@/public/icons/profile.jpg';
import useWindowDimensions from '../hooks/useWindowDimensions';

function calculatePositionOfBlob(node: any, width: number, footerWidth: number) {
    const infos = node.getBoundingClientRect();
    const intX = Math.round(infos.x - ((width - footerWidth) / 2));
    const intWidth = Math.round(infos.width);

    return { x: intX, width: intWidth };
}

function LogoReturnButton() {
    const router = useRouter();
    const { user } = useUser();

    return (
        user.is_anonymous &&
        <Button onClick={() => router.replace('/')} className="absolute top-0 right-3 !shadow-none !p-0 ">
            <Image
                width={100} height={100}
                src={logoIcon} alt='ícone do logotipo'
            />
        </Button>
    );
}

function footerRefCallback(node: any, width: number | undefined, setFooterWidth: (width: number) => void) {
    if (width && node) {
        const intWidth = Math.round(node.getBoundingClientRect().width);
        setFooterWidth(intWidth);
    }
}

interface AsideRefCallbackPropsType {
    node: any,
    path: string,
    width: number | undefined,
    footerWidth: number,
    setCurrentBlobDimensions: (position: { x: number, width: number }) => void
}

function asideRefCallback(props: AsideRefCallbackPropsType) {
    const { node, path, width, footerWidth } = props;
    if (width && node && node.name === path) {
        const position = calculatePositionOfBlob(node, width, footerWidth);
        props.setCurrentBlobDimensions(position);
    }
}

function AsideButtonsJSX() {
    const { user } = useUser();

    const { width } = useWindowDimensions();
    const [footerWidth, setFooterWidth] = useState(0);
    const onFooterRefChange = useCallback((node: any) => {
        footerRefCallback(node, width, setFooterWidth);
    }, [width]);

    const router = useRouter();
    const path = usePathname().split('/')[2];

    const [currentBlobDimensions, setCurrentBlobDimensions] = useState({ x: 0, width: 0 });
    const onRefChange = useCallback((node: any) => {
        const props = { node, path, width, footerWidth, setCurrentBlobDimensions };
        asideRefCallback(props);
    }, [path, width, footerWidth]);

    return (
        <div ref={onFooterRefChange} className="flex justify-around bg-white rounded-t-[25px] px-6 py-3 max-w-md  absolute m-auto inset-x-px bottom-0 backdrop-blur-sm bg-opacity-50 drop-shadow-lg">
            <div style={{
                width: currentBlobDimensions.width,
                left: currentBlobDimensions.x
            }} className='h-[49px] rounded-full bg-primary transition-all duration-500 absolute'></div>
            <AsideButton innerRef={onRefChange} pageName='home' image={homeIcon} onClick={() => router.push('/schedules/home')} />
            <AsideButton innerRef={onRefChange} pageName='mygrades' image={scheduleIcon} onClick={() => router.push('/schedules/mygrades')} />
            {user.is_anonymous ? null : <AsideButton innerRef={onRefChange} pageName='profile' image={profileIcon} onClick={() => router.push('/schedules/profile')} />}
            <AsideButton innerRef={onRefChange} pageName='info' image={infoIcon} onClick={() => router.push('/schedules/info')} />
        </div>
    );
}

function LayoutJSX({ children }: { children: React.ReactNode }) {
    const { breakHeighPoint } = useWindowDimensions();
    const { isLoading } = useUser();

    const path = usePathname().split('/')[2];

    if (isLoading) return <LoadingScreen />;

    return (
        <>
            <InfoHeader />
            <main className={`
                ${path != 'home' ? 'h-[calc(100%-12.75rem)]' :breakHeighPoint ?
                    'pt-3 h-[calc(100%-15.75rem)]' :
                    'pt-7 h-[calc(100%-9.75rem)]'
                }
            `}>
                {children}
            </main>
            <LogoReturnButton />
            <AsideButtonsJSX />
        </>
    );
}

export default function SchedulesLayout({
    children,
}: {
    children: React.ReactNode
}) {

    return (
        <Protected>
            <LayoutJSX>
                {children}
            </LayoutJSX>
        </Protected>
    );
}
