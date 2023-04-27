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
    const [word, setWord] = useState(0);
    const [blocks, setBlocks] = useState(0);
    const [associativity, setAssociativity] = useState(0);
    const [replace, setReplace] = useState(0);
    const [hit, setHit] = useState(1);
    const [miss, setMiss] = useState(20);

    const [dword, dsetWord] = useState(0);
    const [dblocks, dsetBlocks] = useState(0);
    const [dassociativity, dsetAssociativity] = useState(0);
    const [dreplace, dsetReplace] = useState(0);
    const [dhit, dsetHit] = useState(1);
    const [dmiss, dsetMiss] = useState(20);

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
            body: JSON.stringify({
                text: text,
                checked: checked,
                word: word,
                blocks: blocks,
                associativity: associativity,
                replace: replace,
                hit: hit,
                miss: miss,
                dword: dword,
                dblocks: dblocks,
                dassociativity: dassociativity,
                dreplace: dreplace,
                dhit: dhit,
                dmiss: dmiss,
            }),
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

    // for cache
    // I know this is bad but I don't have time to make it better
    const handleWordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            setWord(Number(input));
        }
    };

    const handleBlocksChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            setBlocks(Number(input));
        }
    };

    const handleAssociativityChange = (
        e: React.ChangeEvent<HTMLInputElement>
    ) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            setAssociativity(Number(input));
        }
    };

    const handleReplaceChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setReplace(Number(e.target.value));
        console.log(replace);
    };

    const handleHitChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            setHit(Number(input));
        }
    };

    const handleMissChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            setMiss(Number(input));
        }
    };
    // for cache

    const dhandleWordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            dsetWord(Number(input));
        }
    };

    const dhandleBlocksChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            dsetBlocks(Number(input));
        }
    };

    const dhandleAssociativityChange = (
        e: React.ChangeEvent<HTMLInputElement>
    ) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            dsetAssociativity(Number(input));
        }
    };

    const dhandleReplaceChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        dsetReplace(Number(e.target.value));
        console.log(replace);
    };

    const dhandleHitChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            dsetHit(Number(input));
        }
    };

    const dhandleMissChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const input = e.target.value;
        if (!isNaN(Number(input)) && Number(input) >= 0) {
            dsetMiss(Number(input));
        }
    };

    return (
        <>
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
                <div className="grid md:grid-flow-col md:grid-cols-2 gap-20 items-start mt-10">
                    <div className="flex flex-col space-y-4">
                        <h1 className="text-2xl font-bold mb-4">
                            Instruction Cache
                        </h1>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="word">
                                # word = 2 ^ words_exponent (non-negative)
                                <br />
                                Enter words_exponent
                            </label>
                            <input
                                id="word"
                                type="number"
                                value={word}
                                onChange={handleWordChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="blocks">
                                # blocks = 2 ^ blocks_exponent (non-negative)
                                <br />
                                Enter blocks_exponent
                            </label>
                            <input
                                id="blocks"
                                type="number"
                                value={blocks}
                                onChange={handleBlocksChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="associativity">
                                # associativity = 2 ^ associativity_exponent
                                (non-negative)
                                <br />
                                Enter associativity_exponent
                            </label>
                            <input
                                id="associativity"
                                type="number"
                                value={associativity}
                                onChange={handleAssociativityChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="replace">Replacement Policy</label>
                            <select
                                id="replace"
                                value={replace}
                                onChange={handleReplaceChange}
                                className="border border-gray-400 px-2 py-1"
                            >
                                <option value="0">Select an option</option>
                                <option value="1">
                                    LRU (Least Recently Used)
                                </option>
                                <option value="2">
                                    FIFO (First In First Out)
                                </option>
                                <option value="3">Random</option>
                            </select>
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="hit">Hit Time (non-negative)</label>
                            <input
                                id="hit"
                                type="number"
                                value={hit}
                                onChange={handleHitChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="miss">
                                Miss Penality (non-negative)
                            </label>
                            <input
                                id="miss"
                                type="number"
                                value={miss}
                                onChange={handleMissChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                    </div>
                    <div className="flex flex-col space-y-4">
                        <h1 className="text-2xl font-bold mb-4">Data Cache</h1>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="word">
                                # word = 2 ^ words_exponent (non-negative)
                                <br />
                                Enter words_exponent
                            </label>
                            <input
                                id="word"
                                type="number"
                                value={dword}
                                onChange={dhandleWordChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="blocks">
                                # blocks = 2 ^ blocks_exponent (non-negative)
                                <br />
                                Enter blocks_exponent
                            </label>
                            <input
                                id="blocks"
                                type="number"
                                value={dblocks}
                                onChange={dhandleBlocksChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="associativity">
                                # associativity = 2 ^ associativity_exponent
                                (non-negative)
                                <br />
                                Enter associativity_exponent
                            </label>
                            <input
                                id="associativity"
                                type="number"
                                value={dassociativity}
                                onChange={dhandleAssociativityChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="replace">Replacement Policy</label>
                            <select
                                id="replace"
                                value={dreplace}
                                onChange={dhandleReplaceChange}
                                className="border border-gray-400 px-2 py-1"
                            >
                                <option value="0">Select an option</option>
                                <option value="1">
                                    LRU (Least Recently Used)
                                </option>
                                <option value="2">
                                    FIFO (First In First Out)
                                </option>
                                <option value="3">Random</option>
                            </select>
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="hit">Hit Time (non-negative)</label>
                            <input
                                id="hit"
                                type="number"
                                value={dhit}
                                onChange={dhandleHitChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                        <div className="flex flex-col space-y-1">
                            <label htmlFor="miss">
                                Miss Penality (non-negative)
                            </label>
                            <input
                                id="miss"
                                type="number"
                                value={dmiss}
                                onChange={dhandleMissChange}
                                className="border border-gray-400 px-2 py-1"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
