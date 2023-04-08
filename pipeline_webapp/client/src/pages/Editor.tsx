import ToggleSwitch from "../components/ToggleSwitch";
import { useState } from "react";
import { useText, useUpdateText } from "../context/TextContext";
import { useToggle, useUpdateToggle } from "../context/ToggleContext";
// import useFetch from "../hooks/useFetch";
// import { useEffect } from "react";

export default function Editor() {
    // const [text, setText] = useState("");
    const text = useText();
    const { updateText } = useUpdateText();
    const checked = useToggle();
    const { updateToggle } = useUpdateToggle();
    // const [postId, setPostId] = useState(1);
    // const [checked, setChecked] = useState(true);

    // const { loading, error, value } = useFetch(
    //     "http://127.0.0.1:8000/text",
    //     {
    //         method: "POST",
    //         body: JSON.stringify({ text: text, checked: checked }),
    //     },
    //     [postId]
    // );

    // useEffect(() => {
    //     if (
    //         typeof value === "object" &&
    //         value !== null &&
    //         "success" in value &&
    //         !value.success
    //     )
    //         alert("Invalid Machine Code");
    // }, [postId]);

    function handleClick() {
        fetch("http://127.0.0.1:8000/text", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: text, checked: checked }),
        });
    }

    function handleOnChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
        updateText(e.target.value);
        fetch("http://127.0.0.1:8000/reset")
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert("Invalid Machine Code");
                }
            })
            .catch(error => {
                alert("Invalid Machine Code");
            });
    }

    function handleClear() {
        updateText("");
    }

    return (
        <div className="grid place-items-center p-4 gap-4">
            <h1 className="my-4 text-xl text-emerald-500">Editor</h1>
            <textarea
                className="border-2 resize-none font-mono border-gray-200 text-indigo-600 outline-none focus:border-gray-400 max-w-screen-md w-full"
                rows={16}
                value={text}
                onChange={handleOnChange}
            />
            <div className="flex flex-wrap max-w-screen-md w-full items-center justify-evenly gap-4">
                <button
                    className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-md mt-4"
                    onClick={handleClick}
                >
                    Save
                </button>
                <button
                    className="bg-rose-500 hover:bg-rose-700 text-white font-bold py-2 px-4 rounded-md mt-4"
                    onClick={handleClear}
                >
                    Clear
                </button>
                <ToggleSwitch checked={checked} onChange={updateToggle} />
            </div>
        </div>
    );
}
