'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useCallback, useState } from 'react';
import useUser from '@/app/hooks/useUser';
import useWindowDimensions from '../hooks/useWindowDimensions';
import Image from 'next/image';
import Button from '../components/Button';
import AsideButton from '../components/AsideButton';
import Protected from '../components/Protected';
import InfoHeader from '../components/InfoHeader';
import { LoadingScreen } from '../components/LoadingScreen';
import googleIcon from '@/public/icons/google.jpg';
import { RiCalendarLine } from 'react-icons/ri';
import { FiHome, FiInfo, FiUser } from 'react-icons/fi';

function calculatePositionOfBlob(
  node: any,
  width: number,
  footerWidth: number
) {
  const infos = node.getBoundingClientRect();
  const intX = Math.round(infos.x - (width - footerWidth) / 2);
  const intWidth = Math.round(infos.width);

  return { x: intX, width: intWidth };
}

function LogoReturnButton() {
  const router = useRouter();
  const { user } = useUser();

  return (
    user.is_anonymous && (
      <Button
        onClick={() => router.replace('/')}
        className="fixed z-[6] top-4 right-6 !shadow-none !p-0 "
      >
        <div className="bg-white flex justify-center items-center rounded-full w-12 h-12">
          <Image
            width={35}
            height={35}
            src={googleIcon}
            alt="ícone do logotipo google"
          />
        </div>
      </Button>
    )
  );
}

function footerRefCallback(
  node: any,
  width: number | undefined,
  setFooterWidth: (width: number) => void
) {
  if (width && node) {
    const intWidth = Math.round(node.getBoundingClientRect().width);
    setFooterWidth(intWidth);
  }
}

interface AsideRefCallbackPropsType {
  node: any;
  path: string;
  width: number | undefined;
  footerWidth: number;
  setCurrentBlobDimensions: (position: { x: number; width: number }) => void;
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
  const onFooterRefChange = useCallback(
    (node: any) => {
      footerRefCallback(node, width, setFooterWidth);
    },
    [width]
  );

  const router = useRouter();
  const path = usePathname().split('/')[2];

  const [currentBlobDimensions, setCurrentBlobDimensions] = useState({
    x: 0,
    width: 0,
  });
  const onRefChange = useCallback(
    (node: any) => {
      const props = {
        node,
        path,
        width,
        footerWidth,
        setCurrentBlobDimensions,
      };
      asideRefCallback(props);
    },
    [path, width, footerWidth]
  );

  return (
    <div
      ref={onFooterRefChange}
      className="flex justify-around bg-white rounded-t-[25px] px-6 py-3 max-w-md fixed b-0 m-auto inset-x-px bottom-0 backdrop-blur-sm bg-opacity-50 drop-shadow-lg"
    >
      <div
        style={{
          width: currentBlobDimensions.width,
          left: currentBlobDimensions.x,
        }}
        className="h-[49px] rounded-full bg-primary transition-all duration-500 absolute"
      ></div>
      <AsideButton
        innerRef={onRefChange}
        pageName="home"
        image={<FiHome className="text-2xl" />}
        onClick={() => router.push('/schedules/home')}
      />
      <AsideButton
        innerRef={onRefChange}
        pageName="mygrades"
        image={<RiCalendarLine className="text-2xl" />}
        onClick={() => router.push('/schedules/mygrades')}
      />
      {user.is_anonymous ? null : (
        <AsideButton
          innerRef={onRefChange}
          pageName="profile"
          image={<FiUser className="text-2xl" />}
          onClick={() => router.push('/schedules/profile')}
        />
      )}
      <AsideButton
        innerRef={onRefChange}
        pageName="info"
        image={<FiInfo className="text-2xl" />}
        onClick={() => router.push('/schedules/info')}
      />
    </div>
  );
}

function LayoutJSX({ children }: { children: React.ReactNode }) {
  const { breakHeighPoint } = useWindowDimensions();
  const { isLoading } = useUser();

  return (
    <>
      <InfoHeader />
      {!isLoading ? (
        <main className={`${breakHeighPoint ? 'pt-[136px]' : 'pt-16'} pb-36`}>
          {children}
        </main>
      ) : (
        <LoadingScreen />
      )}
      <LogoReturnButton />
      <AsideButtonsJSX />
    </>
  );
}

export default function SchedulesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <Protected>
      <LayoutJSX>{children}</LayoutJSX>
    </Protected>
  );
}
