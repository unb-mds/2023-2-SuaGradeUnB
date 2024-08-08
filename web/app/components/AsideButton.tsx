import Image, { StaticImageData } from 'next/image';

import Button from './Button';

interface AsideButtonPropsType {
  image: React.ReactNode;
  pageName: string;
  innerRef?: (node: any) => void;
  onClick?: () => void;
}

export default function AsideButton({
  image,
  pageName,
  innerRef,
  onClick,
}: AsideButtonPropsType) {
  return (
    <Button
      innerRef={innerRef}
      onClick={onClick}
      className="z-10 flex-col w-full !gap-1 !pb-2 !shadow-none !text-black"
      name={pageName}
    >
      {image}
    </Button>
  );
}
