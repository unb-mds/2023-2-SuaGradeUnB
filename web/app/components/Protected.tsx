'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useEffect } from 'react';

import useUser from '../hooks/useUser';

const protectedRoutes = ['/schedules/profile'];

interface ProtectedPropsType {
    children: React.ReactNode;
}

export default function Protected({ children }: ProtectedPropsType) {
    const { user, isLoading } = useUser();
    const path = usePathname();
    const router = useRouter();

    useEffect(() => {
        if (!isLoading) {
            if (user.is_anonymous && protectedRoutes.includes(path)) {
                router.replace('/');
            }
        }
    }, [user.is_anonymous, isLoading, path, router]);

    if (user.is_anonymous && protectedRoutes.includes(path)) return null;

    return children;
}