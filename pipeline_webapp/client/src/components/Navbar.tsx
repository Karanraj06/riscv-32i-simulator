import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <nav className="bg-slate-500 text-white py-4">
            <div className="container mx-auto flex justify-between items-center">
                <div>
                    <Link to="/" className="font-bold text-xl">
                        RISCV-32I Simulator
                    </Link>
                </div>
                <div>
                    <ul className="flex">
                        <li>
                            <Link
                                to="http://karanraj.pythonanywhere.com/"
                                className="px-4 py-2 hover:text-gray-300"
                            >
                                Single Cycle Execution
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/"
                                className="px-4 py-2 hover:text-gray-300"
                            >
                                Editor
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/simulator"
                                className="px-4 py-2 hover:text-gray-300"
                            >
                                Simulator
                            </Link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
}
