import { useEffect, useState } from 'react';

type WindowDimentions = {
    width: number | undefined;
    height: number | undefined;
    breakHeighPoint: boolean;
};

const useWindowDimensions = (): WindowDimentions => {
    const [windowDimensions, setWindowDimensions] = useState<WindowDimentions>({
        width: undefined,
        height: undefined,
        breakHeighPoint: false
    });

    useEffect(() => {
        function handleResize(): void {
            setWindowDimensions({
                width: window.innerWidth,
                height: window.innerHeight,
                breakHeighPoint: window.innerHeight >= 490
            });
        }

        handleResize();
        window.addEventListener('resize', handleResize);

        return (): void => window.removeEventListener('resize', handleResize);
    }, []);

    return windowDimensions;
};

export default useWindowDimensions;