import { useContext, useState, createContext, ReactNode } from "react";

interface ToggleProviderProps {
    children: ReactNode;
}

interface ToggleUpdateContext {
    updateToggle: () => void;
}

const ToggleContext = createContext<boolean>(true);

const ToggleUpdateContext = createContext<ToggleUpdateContext>({
    updateToggle: () => {},
});

export function useToggle() {
    return useContext(ToggleContext);
}

export function useUpdateToggle() {
    return useContext(ToggleUpdateContext);
}

export function ToggleProvider({ children }: ToggleProviderProps) {
    const [toggle, setToggle] = useState<boolean>(true);

    function updateToggle() {
        setToggle(prevToggle => !prevToggle);
    }

    return (
        <ToggleContext.Provider value={toggle}>
            <ToggleUpdateContext.Provider value={{ updateToggle }}>
                {children}
            </ToggleUpdateContext.Provider>
        </ToggleContext.Provider>
    );
}
