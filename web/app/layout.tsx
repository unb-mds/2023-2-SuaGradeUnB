import type { Metadata } from 'next';

import { Poppins } from 'next/font/google';
import './globals.css';

import UserContextProvider from './contexts/UserContext';
import YearPeriodContextProvider from './contexts/YearPeriodContext';
import ClassesToShowContextProvider from './contexts/ClassesToShowContext';
import SelectedClassesContextProvider from './contexts/SelectedClassesContext/SelectedClassesContext';
import SchedulesContextProvider from './contexts/SchedulesContext';
import ModalContextProvider from './contexts/ModalContext';

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
      <body className={`${poppins.variable} h-screen font-sans bg-white`}>
        <Toaster />
        <UserContextProvider>
          <YearPeriodContextProvider>
            <ClassesToShowContextProvider>
              <SelectedClassesContextProvider>
                <ModalContextProvider>
                  <SchedulesContextProvider>
                    {children}
                  </SchedulesContextProvider>
                </ModalContextProvider>
              </SelectedClassesContextProvider>
            </ClassesToShowContextProvider>
          </YearPeriodContextProvider>
        </UserContextProvider>
      </body>
    </html>
  );
}
