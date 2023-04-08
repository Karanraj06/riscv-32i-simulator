import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Editor from "./pages/Editor";
import Simulator from "./pages/Simulator";

export default function App() {
    return (
        <>
            <Navbar />
            <Routes>
                <Route path="/" element={<Editor />} />
                <Route path="/simulator" element={<Simulator />} />
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
        </>
    );
}
