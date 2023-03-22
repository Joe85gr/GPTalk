import React, { useEffect, useRef, useState } from 'react';
import ReactDOM from 'react-dom';
import { ScrollDivToRef, FilterMessages, ScrollToRef, Timeout } from './Utilities'
import { ChatMessage } from './components/Messages';
import { TypingAnimation } from './components/TypingAnimation';
import { Input } from './components/Input';
import { ModelSelect, ModelsProps } from './components/ModelSelect';
import { Configuration } from './global';
import { LoadModels, GetReply, CreateChat, GetConversation, GetConversations, Message, ModelReply } from './infrastructure/Api'

import './App.css';
import './normal.css';

function App() {
  const defaultModels: ModelsProps[] = [
    { label: "gpt-3.5-turbo", value: "gpt-3.5-turbo" },
  ];

  const defaultMessage: Message[] = [ 
    {role: "system", content: Configuration.GPT_BEHAVIOUR},
  ] 

  const currentChatId = window.localStorage.getItem('chat_id');

  const [input, setInput] = useState("");

  let [model, setModel] = useState(defaultModels[0].value);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const conversations: ModelReply[] = []
  const [storedConversations, setStoredConversations] = useState(conversations);

  const [chatId, setChatId] = useState(currentChatId);

  const initialChatLog: ModelReply = { 
    messages:defaultMessage, 
    total_tokens: 0, 
    chat_id: chatId ? chatId : undefined,
    model,
    chat_description: "new chat"};
  
  const [chatLog, setChatLog] = useState(initialChatLog);
  const [models, setModels] = useState(defaultModels);

  const messagesEndRef = useRef<HTMLDivElement>(null); 
  const chatRefs = useRef<HTMLDivElement>(null); 

  useEffect(() => {

  ScrollNavbar();

  }, [storedConversations]);

  useEffect(() => {
    ScrollDivToRef(messagesEndRef)
    
  }, [chatLog]);

  async function ScrollNavbar(chatid?: string) { 
    await Timeout(500);
    console.log("chatRefs triggered");
    let id;
    if(chatid) {
      id = chatid;
    } else { 
      id = chatId;
    }
    let form = document.getElementById(`chat-${id}`);
    console.log(form);
    if(form) { 
      ScrollToRef(form);
    }
}

  async function newChat(){
    window.localStorage.removeItem('chat_id');

    const response = await CreateChat();
    setChatLog(response);

    console.log("newChat response", response);
    if(response.chat_id){
      window.localStorage.setItem('chat_id', String(response.chat_id));
      setChatId(String(response.chat_id))
    }
    loadChats();
  }

  async function loadChat(chatId: number) {

    const response = await GetConversation(chatId);
    setChatLog(response);

    console.log("loadChat response", response);
    if(response.chat_id){
      window.localStorage.setItem('chat_id', String(response.chat_id));
      setChatId(String(response.chat_id));
      ScrollNavbar(response.chat_id)
    }
  }

  async function loadChats() { 
    const storedConversations = await GetConversations();
    if(storedConversations) {
      setStoredConversations(storedConversations)
      console.log("storedConversations:", storedConversations);
    } else { 
      console.log("No storedConversations.");
     }
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

    async function loadChatLog(chatId: number) {
      const storedConversation = await GetConversation(chatId);

      if(storedConversation){
        setChatLog(storedConversation);
      } else {
        window.localStorage.removeItem('chat_id');
        await newChat()
      }
     }

    loadModels();
    loadChats();

    if(currentChatId) {
      loadChatLog(Number(currentChatId));
    }
  }, [])

  async function handleSubmit(e: React.SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();

    if (input.length === 0) {
      return;
    }

    setIsLoading(true);

    if(chatId === null || chatId === undefined){
      await newChat();
    }
    const message = { "role": "user", "content": input};
    setInput("");

    const newChatLog: ModelReply = { 
      messages: [...chatLog.messages, message], 
      total_tokens: 1, 
      chat_id: chatLog.chat_id,
      model,
      chat_description: chatLog.chat_description};

    setChatLog(newChatLog);

    const request: ModelReply = { 
      messages: newChatLog.messages.filter((message) => FilterMessages(message, "error")),
      total_tokens: newChatLog.total_tokens, 
      chat_id: newChatLog.chat_id,
      model,
      chat_description: newChatLog.chat_description};

    const data = await GetReply(request);

    setChatLog(data);
    setIsLoading(false);
  }

  return (
    <div id="main">
      <div className="navbar">
        <div className="nav-container">
          <a className="nav-button nav-item" onClick={newChat}>
            New Chat
          </a>
        </div>
        <div className="nav-container-middle nav-border nav-hide">
        {
          storedConversations
                .map((modelReply, i) => (
                  <a id={`chat-${modelReply.chat_id}`} 
                      className={`nav-chats ${chatId == modelReply.chat_id && 'nav-chats-current'}`} 
                      key={modelReply.chat_id} 
                      onClick={() => loadChat(Number(modelReply.chat_id))}>
                    {modelReply.chat_id}
                    { modelReply.chat_id == chatId && <div ref={chatRefs} />}
                  </a>
              ))
            }
        </div>
        <div className="nav-container nav-container-secondary nav-border-top">
          <div className='nav-info nav-hide '>
              Model
          </div>
          <ModelSelect 
            models={models} 
            defaultModel={defaultModels[0].value}
            setModel={setModel}/>
        </div>
      </div>

      <div className="main-container">
        {
          chatLog
            .messages
            .filter((message: Message) => FilterMessages(message, "system"))
            .map((message, i) => (
              <ChatMessage key={i} {...message}/> 
          ))
        }
      { !chatId && <div className='new-chat'> Create new Chat to start</div>}
  
      <div ref={messagesEndRef} />
        {isLoading && <TypingAnimation />}
      </div>
      { chatId && <div>
      <div className="footer-info">Total Tokens: {chatLog.total_tokens}</div>
        <Input
          handleSubmit={handleSubmit} 
          onEnterPress={onEnterPress}
          setInput={setInput}
          input={input}
          /> 
          </div>}
    </div>

  );
}

export default App
