import Button from './Button';

interface AsideButtonPropsType {
    icon: string;
    text: string;
    onClick?: () => void;
}


export default function AsideButton({ icon, text, onClick }: AsideButtonPropsType) {
    return (
        <Button onClick={onClick} className='z-10 flex-col !p-0 !gap-1 !shadow-none'>
            <span className="material-symbols-rounded">
                {icon}
            </span>
            <span>
                {text}
            </span>
        </Button>
    );
}