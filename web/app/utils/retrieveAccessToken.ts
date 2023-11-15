export default function retrieveAccessToken(): string | undefined {
    let access_token: string | undefined = undefined;

    const fullUrl = window.location.href;
    const urlParts = fullUrl.split('#');

    if (urlParts.length > 1) {
        const fragment = urlParts[1];
        const params = fragment.split('&');

        params.forEach(param => {
            const [key, value] = param.split('=');
            if (key === 'access_token') access_token = value;
        });
    }

    return access_token;
}