import type { Metadata } from 'next';

import { Poppins, Chivo_Mono } from 'next/font/google';
import './globals.css';

import UserContextProvider from './contexts/UserContext';
import YearPeriodContextProvider from './contexts/YearPeriodContext';
import ClassesToShowContextProvider from './contexts/ClassesToShowContext';
import SelectedClassesContextProvider from './contexts/SelectedClassesContext/SelectedClassesContext';
import SchedulesContextProvider from './contexts/SchedulesContext';

import { Toaster } from 'react-hot-toast';
import { TooltipProvider } from './components/ui/tooltip';

export const poppins = Poppins({
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
  style: ['normal', 'italic'],
  subsets: ['latin'],
  variable: '--font-poppins',
});

export const chivoMono = Chivo_Mono({
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
  style: ['normal', 'italic'],
  subsets: ['latin'],
  variable: '--font-chivo-mono',
});

export const metadata: Metadata = {
  title: 'Sua Grade UnB',
  description: 'Aplicação para gerenciamento de grade de horários da UnB',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`${poppins.variable} ${chivoMono.variable} max-h-screen font-sans bg-white`}
      >
        <Toaster />
        <SchedulesContextProvider>
          <UserContextProvider>
            <YearPeriodContextProvider>
              <ClassesToShowContextProvider>
                <SelectedClassesContextProvider>
                  <TooltipProvider>{children}</TooltipProvider>
                </SelectedClassesContextProvider>
              </ClassesToShowContextProvider>
            </YearPeriodContextProvider>
          </UserContextProvider>
        </SchedulesContextProvider>
      </body>
    </html>
  );
}
