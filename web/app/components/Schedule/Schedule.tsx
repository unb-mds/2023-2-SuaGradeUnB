export default function Schedule() {
    const days = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
    const times = [
        '08:00 - 08:55', '08:55 - 09:50', '10:00 - 10:55',
        '10:55 - 11:50', '12:00 - 12:55', '12:55 - 13:50',
        '14:00 - 14:55', '14:55 - 15:50', '16:00 - 16:55',
        '16:55 - 17:50', '18:00 - 18:55', '19:00 - 19:50',
        '19:50 - 20:40', '20:50 - 21:40', '21:40 - 22:30'
    ];

    return (
        <>
            <div className="flex justify-end">
                <div className="w-40"></div>
                <div className="flex">
                    {days.map((day, index) => 
                        <div key={index} className="text-center w-24">
                            {day}
                        </div>
                    )}
                </div>
            </div>
            <div>
                {times.map((time, index) =>
                    <div className="flex" key={index}>
                        <div className="flex justify-center items-center font-mono w-40">
                            {time}
                        </div>
                        <div className="flex">
                            {days.map((day, index) => 
                                <div key={index} className="flex justify-center items-center w-24">
                                    FGA0053
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}