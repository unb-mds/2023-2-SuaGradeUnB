'use client';

import { usePathname, useRouter } from 'next/navigation';
import useUser from '@/app/hooks/useUser';

import AsideButton from '../components/AsideButton';
import Protected from '../components/Protected';
import { LoadingScreen } from '../components/LoadingScreen';
import InfoHeader from '../components/InfoHeader';

import homeIcon from '@/public/icons/home.jpg';
import scheduleIcon from '@/public/icons/schedule.jpg';
import profileIcon from '@/public/icons/profile.jpg';
import useWindowDimensions from '../hooks/useWindowDimensions';

function LayoutJSX({ children }: { children: React.ReactNode }) {
    const { breakHeighPoint } = useWindowDimensions();
    const { user, isLoading } = useUser();

    const router = useRouter();
    const path = usePathname().split('/')[2];

    if (isLoading) return <LoadingScreen />;

    return (
        <>
            <InfoHeader />
            <main className={`${breakHeighPoint ? 'pt-3 h-[calc(100%-15.75rem)]' : 'pt-7 h-[calc(100%-9.75rem)]'}`}>
                {children}
            </main>
            <div className="flex justify-around bg-white rounded-t-[25px] px-6 py-3 max-w-md  absolute m-auto inset-x-px bottom-0 backdrop-blur-sm bg-opacity-50 drop-shadow-lg">
                <section className={`grid grid-cols-${user.is_anonymous ? '2' : '3'} px-6 absolute w-full`}>
                    <div className={
                        `h-[49px] rounded-full bg-primary transition-all duration-300
                        ${path === 'home' ? 'col-start-1' : (path === 'mygrades' ? 'col-start-2' : 'col-start-3')}
                    `}></div>
                </section>
                <AsideButton image={homeIcon} text='' onClick={() => router.push('/schedules/home')} />
                <AsideButton image={scheduleIcon} text='' onClick={() => router.push('/schedules/mygrades')} />
                {user.is_anonymous ? null : <AsideButton image={profileIcon} text='' onClick={() => router.push('/schedules/profile')} />}
            </div>
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
