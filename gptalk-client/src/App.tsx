import React, { useEffect, useRef, useState } from 'react';
import ReactDOM from 'react-dom';
import { ScrollToBottom, FilterMessages } from './Utilities'
import { ChatMessage, IMessage } from './components/Messages';
import { TypingAnimation } from './components/TypingAnimation';
import { Input } from './components/Input';
import { ModelSelect, ModelsProps } from './components/ModelSelect';
import { Configuration } from './global';
import { LoadModels, GetReply } from './infrastructure/Api'

import './App.css';
import './normal.css';

function App() {
  const defaultModels: ModelsProps[] = [
    { label: "gpt-3.5-turbo", value: "gpt-3.5-turbo" },
  ];

  const defaultMessage: IMessage[] = [ 
    {role: "system", content: Configuration.GPT_BEHAVIOUR},
  ] 

  const storedChatLog = window.localStorage.getItem('chatLog');

  const initialMessage: IMessage[] = storedChatLog == null 
    ? defaultMessage
    : JSON.parse(storedChatLog);

  const [input, setInput] = useState("");
  const [totalTokens, setTotalTokens] = useState(
    window.localStorage.getItem('total_tokens') == null
      ? "0"
      : window.localStorage.getItem('total_tokens'));

  let [model, setModel] = useState(defaultModels[0].value);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const [chatLog, setChatLog] = useState(initialMessage);
  const [models, setModels] = useState(defaultModels);

  const messagesEndRef = useRef<HTMLDivElement>(null); 

  useEffect(() => {
    ScrollToBottom(messagesEndRef)
  }, [chatLog]);

  function clearChat(){
    window.localStorage.removeItem('chatLog');
    window.localStorage.removeItem('total_tokens');
    setTotalTokens("0");
    setChatLog(defaultMessage);
  }

  const onEnterPress = (e: React.KeyboardEvent) => {
    if(e.code == "Enter" && e.shiftKey == false && isLoading == false ) {
      e.preventDefault();
      let form = document.getElementById('chat-button');
      if(form) { 
        (form as HTMLFormElement).click(); 
      }
    }
  }

  useEffect(() => {
    async function loadModels() {
      const models = await LoadModels();
      setModels(models);
    }
    loadModels();
  }, [])

  async function handleSubmit(e: React.SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();

    if (input.length === 0) {
      return;
    }

    setIsLoading(true);

    const message = { "role": "user", "content": input};
    setInput("");

    const newChatLog = [...chatLog, message];
    window.localStorage.setItem('chatLog', JSON.stringify(newChatLog));

    setChatLog([...chatLog, message]);

    const messages = newChatLog.filter((message) => FilterMessages(message, "error"));

    const data = await GetReply(messages, model);

    window.localStorage.setItem('chatLog', JSON.stringify(data.messages));
    window.localStorage.setItem('total_tokens', JSON.stringify(data.total_tokens));

    setTotalTokens(data.total_tokens);
    setChatLog(data.messages);
    setIsLoading(false);
  }

  return (
    <div id="main">
      <div className="navbar">
        <div className="nav-container nav-border">
          <a className="nav-button nav-item" onClick={clearChat}>
            New Chat
          </a>
        </div>
        <div className="nav-container nav-container-secondary">
          <div className='nav-info'>
              Model
          </div>
          <ModelSelect 
            models={models} 
            defaultModel={defaultModels[0].value}
            setModel={setModel}/>
        </div>
      </div>

      <div className="main-container">

        {chatLog
          .filter((message: IMessage) => FilterMessages(message, "system"))
          .map((message, index) => (
          <ChatMessage key={index} {...message}/>
        ))}
  
      <div ref={messagesEndRef} />
        {isLoading && <TypingAnimation />}
      </div>
      <div className="footer-info">Total Tokens: {totalTokens}</div>
        <Input
          handleSubmit={handleSubmit} 
          onEnterPress={onEnterPress}
          setInput={setInput}
          input={input}
          />
    </div>

  );
}

export default App
