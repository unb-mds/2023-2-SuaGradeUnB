interface DisciplineBoxPropsType {
    name: string,
    code: string,
    teachers: Array<string>,
    schedule: string
}

export default function DisciplineBox(props: DisciplineBoxPropsType) {
    return (
        <span className='flex items-center justify-between rounded-lg font-semibold w-10/12 max-h-28 py-2 px-4 shadow-lg bg-snow-primary text-sm'>
            <div className='flex flex-col gap-1'>
                <section>
                    {props.name} - {props.code}
                </section>
                {props.teachers.length && (
                    <section>
                        {props.teachers[0]} {props.teachers.length > 1 && 'e outros'}
                    </section>
                )}
                <section>{props.schedule}</section>
            </div>
            <button className='material-symbols-rounded hover:text-red-900'>
                delete
            </button>
        </span>
    );
}