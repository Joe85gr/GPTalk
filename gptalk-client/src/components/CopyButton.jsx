import React, { useState } from "react";
import { SvgCopy, Ok } from "./Svg"

export function CodeCopyBtn(children) {

    const [clicked, setClicked] = useState(false);

    const handleClick = (e) => {
        if(children) {
            navigator.clipboard.writeText(children[0].props.children[0]);

        }
        setClicked(true)
        
        setTimeout(() => {
            setClicked(false);
        }, 2000);
    }

    return (
        <div className="absolute transition hover:bg-gray-800 p-1 rounded-md right-2 top-3 cursor-pointer border-1">
            <i className='' onClick={handleClick} >
                { clicked? <Ok /> : <SvgCopy />  }
            </i>
        </div>
    )
}
