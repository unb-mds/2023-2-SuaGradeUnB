import Link from 'next/link';

export default function NotFound() {
    return (
        <div className='flex flex-col justify-between min-h-screen z-10'>
            <div></div>
            <main className='flex flex-col justify-center items-center h-full'>
                <h1 className='text-2xl font-semibold'>404 Not Found</h1>
                <p>A página que você está procurando não existe.</p>
                <p>
                    Voltar para o <Link href="/" className='underline'>início</Link>
                </p>
            </main>
            <footer className='flex items-center justify-center p-3'>Sua Grade UnB</footer>
        </div>
    );
}