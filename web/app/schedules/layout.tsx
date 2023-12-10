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
import googleIcon from '@/public/icons/google.jpg';
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
        <Button onClick={() => router.replace('/')} className="absolute top-4 right-6 !shadow-none !p-0 ">
            <div className="bg-white flex justify-center items-center rounded-full w-12 h-12">
                <Image 
                    width={35} height={35}
                    src={googleIcon} alt='ícone do logotipo google'
                />
            </div>
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

function getMainClassName(path: string, breakHeighPoint: boolean) {
    const baseClassName = breakHeighPoint ? 'h-[calc(100%-15.75rem)]' : 'h-[calc(100%-9.75rem)]';
    return path !== 'home' ? baseClassName : `pt-${breakHeighPoint ? 3 : 7} ${baseClassName}`;
}

function LayoutJSX({ children }: { children: React.ReactNode }) {
    const { breakHeighPoint } = useWindowDimensions();
    const { isLoading } = useUser();
    const path = usePathname().split('/')[2];

    if (isLoading) return <LoadingScreen />;

    const mainClassName = getMainClassName(path, breakHeighPoint);

    return (
        <>
            <InfoHeader />
            <main className={mainClassName}>
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
