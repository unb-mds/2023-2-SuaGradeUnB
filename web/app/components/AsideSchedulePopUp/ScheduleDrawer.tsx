import AddDisciplineButton from '@/app/schedules/home/components/AddDisciplineButton';
import {
  Drawer,
  DrawerContent,
  DrawerTitle,
  DrawerTrigger,
} from '../ui/drawer';
import { ScheduleDrawerContent } from './ScheduleDrawerContent';

export const ScheduleDrawer = () => {
  return (
    <Drawer>
      <DrawerTrigger>
        <AddDisciplineButton />
      </DrawerTrigger>

      <DrawerContent
        className="max-w-2xl bg-snow-primary h-full max-h-[75vh] rounded-t-[2.5rem] sm:mx-auto mx-6 shadow-lg border-0"
        showOverlay={false}
      >
        <ScheduleDrawerContent />
      </DrawerContent>
    </Drawer>
  );
};
