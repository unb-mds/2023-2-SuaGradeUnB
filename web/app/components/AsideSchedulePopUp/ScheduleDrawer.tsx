import AddDisciplineButton from '@/app/schedules/home/components/AddDisciplineButton';
import { Drawer, DrawerContent, DrawerTrigger } from '../ui/drawer';
import { ScheduleDrawerContent } from './ScheduleDrawerContent';

export const ScheduleDrawer = () => {
  return (
    <Drawer>
      <DrawerTrigger>
        <AddDisciplineButton />
      </DrawerTrigger>

      <DrawerContent
        className="max-w-2xl bg-snow-secondary h-full max-h-[82%] rounded-t-[2.5rem] sm:mx-auto mx-6 shadow-lg border-0"
        showOverlay={false}
        hideDragIndicator
      >
        <ScheduleDrawerContent />
      </DrawerContent>
    </Drawer>
  );
};
