import { AppRouterInstance } from 'next/dist/shared/lib/app-router-context.shared-runtime';

export default function signInWithGoogle(router: AppRouterInstance) {
    const tokenEndpoint = process.env.NEXT_PUBLIC_GOOGLE_OAUTH_URL;

    const clientId = process.env.NEXT_PUBLIC_GOOGLE_OAUTH_CLIENT_ID || '';
    const redirectUri = 'http://localhost:3000';
    const scope = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ].join(' ');

    const params = new URLSearchParams({
        client_id: clientId,
        redirect_uri: redirectUri,
        scope: scope,
        include_granted_scopes: 'false',
        access_type: 'online',
        state: 'pass-through-value',
        response_type: 'token',
    });

    const url = `${tokenEndpoint}?${params}`;
    router.replace(url);
}