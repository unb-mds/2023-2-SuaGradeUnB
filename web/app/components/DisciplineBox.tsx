interface DisciplineBoxPropsType {
    name: string,
    code: string,
    teachers: Array<string>,
    schedule: string
}

export default function DisciplineBox(props: DisciplineBoxPropsType) {
    return (
        <span className='flex flex-col justify-center gap-1 rounded-lg font-semibold w-10/12 max-h-28 py-2 px-4 mx-4 shadow-lg hover:shadow-md bg-slate-200/100 text-sm'>
            <section>
                {props.name} - {props.code}
            </section>
            <section>
                {props.teachers[0]} {props.teachers.length > 1 ? 'e outros' : ''}
            </section>
            <section>{props.schedule}</section>
        </span>
    );
}