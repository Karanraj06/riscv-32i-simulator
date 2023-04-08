interface StatsProps {
    label: string;
    val: number;
}

export default function Stats({ label, val }: StatsProps) {
    return (
        <div className="flex justify-center my-2">
            <div className="flex justify-between max-w-screen-md w-full text-xl mx-2">
                <div className="text-emerald-500"># {label}</div>
                <div className="border border-gray-200 hover:border-emerald-400 w-28 rounded-sm text-center font-mono text-gray-400">
                    {val}
                </div>
            </div>
        </div>
    );
}
