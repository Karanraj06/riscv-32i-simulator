import { useContext, useState, createContext, ReactNode } from 'react';

interface TextProviderProps {
  children: ReactNode;
}

interface TextUpdateContext {
  updateText: (newText: string) => void;
}

const TextContext = createContext<string>('');

const TextUpdateContext = createContext<TextUpdateContext>({
  updateText: () => {},
});

export function useText() {
  return useContext(TextContext);
}

export function useUpdateText() {
  return useContext(TextUpdateContext);
}

export function TextProvider({ children }: TextProviderProps) {
  const [text, setText] = useState<string>(String());

  function updateText(newText: string) {
    setText(newText);
  }

  return (
    <TextContext.Provider value={text}>
      <TextUpdateContext.Provider value={{ updateText }}>
        {children}
      </TextUpdateContext.Provider>
    </TextContext.Provider>
  );
}
