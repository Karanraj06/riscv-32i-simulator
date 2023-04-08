interface ToggleSwitchProps {
    checked: boolean;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function ToggleSwitch({ checked, onChange }: ToggleSwitchProps) {
    return (
        <label className="relative inline-flex items-center mr-5 cursor-pointer">
            <input
                type="checkbox"
                checked={checked}
                className="sr-only peer"
                onChange={onChange}
            />
            <div className="w-11 h-6 bg-gray-200 rounded-full peer dark:bg-gray-700 peer-focus:ring-4 peer-focus:ring-rose-300 dark:peer-focus:ring-rose-800 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-rose-600" />
            <span className="ml-3 text-sm font-medium text-gray-900 dark:text-gray-300">
                Enable Forwarding
            </span>
        </label>
    );
}
