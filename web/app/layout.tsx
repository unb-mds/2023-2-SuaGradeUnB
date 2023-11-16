import type { Metadata } from 'next';

import { Poppins } from 'next/font/google';
import './globals.css';

import UserContextProvider from './contexts/UserContext';

import { Toaster } from 'react-hot-toast';

const poppins = Poppins({
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
  style: ['normal', 'italic'],
  subsets: ['latin'],
  variable: '--font-poppins',
});

export const metadata: Metadata = {
  title: 'Sua Grade UnB',
  description: 'Aplicação para gerenciamento de grade de horários da UnB',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${poppins.variable} font-sans bg-white`}>
        <Toaster />
        <UserContextProvider>
          {children}
        </UserContextProvider>
      </body>
    </html>
  );
}
