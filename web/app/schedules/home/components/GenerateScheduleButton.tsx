'use router';

import { useRouter } from 'next/navigation';
import useClassesToShow from '@/app/hooks/useClassesToShow';

import Button from '@/app/components/Button';

export default function GenerateScheduleButton() {
    const router = useRouter();

    const { classesToShow } = useClassesToShow();

    return (
        <div className='flex justify-center'>
            <Button
                disabled={classesToShow.length === 0}
                onClick={() => router.replace('/schedules/mygrades')}
                className='absolute bottom-28 w-52 h-10 font-semibold bg-primary disabled:opacity-70'
            >
                Gerar Grade
            </Button>
        </div>
    );
}