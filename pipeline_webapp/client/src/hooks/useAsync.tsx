import { useCallback, useEffect, useState } from 'react';

interface AsyncResult<T> {
  loading: boolean;
  error?: Error;
  value?: T;
}

export default function useAsync<T>(
  callback: () => Promise<T>,
  dependencies: any[] = []
): AsyncResult<T> {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error>();
  const [value, setValue] = useState<T>();

  const callbackMemoized = useCallback(() => {
    setLoading(true);
    setError(undefined);
    setValue(undefined);
    callback()
      .then(setValue)
      .catch(setError)
      .finally(() => setLoading(false));
  }, dependencies);

  useEffect(() => {
    callbackMemoized();
  }, [callbackMemoized]);

  return { loading, error, value };
}
