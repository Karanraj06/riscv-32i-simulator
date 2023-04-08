import useAsync from "./useAsync";

interface Options {
    headers?: Record<string, string>;
    method?: string;
    body?: string;
}

const DEFAULT_OPTIONS: Options = {
    headers: { "Content-Type": "application/json" },
};

export default function useFetch<T>(
    url: string,
    options: Options = {},
    dependencies: any[] = []
) {
    return useAsync<T>(() => {
        return fetch(url, { ...DEFAULT_OPTIONS, ...options }).then(res => {
            if (res.ok) return res.json();
            return res.json().then(json => Promise.reject(json));
        });
    }, dependencies);
}
