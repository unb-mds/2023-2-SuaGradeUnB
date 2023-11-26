
import styles from '@/app/styles/tooltip.module.css';

interface TooltipPropsType {
    children: React.ReactNode
};

export default function Tooltip({ children }: TooltipPropsType) {
    return (
        <div className={styles.tooltip}>
            <span className='flex justify-center items-center material-symbols-rounded text-xs border-black border-solid border-2 rounded-full h-5 w-5'>
                question_mark
            </span>
            <span className={`${styles.tooltiptext} p-2`}>
                {children}
            </span>
        </div>
    );
}