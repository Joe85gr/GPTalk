import React from 'react';

import './Input.css'

interface Props {
    handleSubmit: (e: React.SyntheticEvent<HTMLFormElement>) => Promise<void>;
    onEnterPress: (e: React.KeyboardEvent) => void;
    setInput: (value: string) => void;
    input: string;
}

export const Input: React.FC<Props> = (props) => {
    return (
        <form id="chat-form" className="footer" onSubmit={props.handleSubmit}>
          <div className="input-container">
            <textarea 
              rows={1}
              className='chat-input' 
              onKeyDown={props.onEnterPress}
              value={props.input}
              onChange={(e) => props.setInput(e.target.value)}>
            </textarea >
            <button id="chat-button" type="submit" style={{display: "none"}}>
            </button>
          </div>
        </form>
    )
  }