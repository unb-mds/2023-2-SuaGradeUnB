import Button from '@/app/components/Button';
import useWindowDimensions from '@/app/hooks/useWindowDimensions';

export default function AddDisciplineButton() {
  const { breakHeighPoint } = useWindowDimensions();

  return (
    <div className="flex justify-center w-[100vw]">
      <Button
        className={`fixed ${
          breakHeighPoint ? 'top-20' : 'top-3'
        } z-[6] font-semibold bg-secondary`}
      >
        Buscar matéria
      </Button>
    </div>
  );
}
