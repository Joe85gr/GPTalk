import React, { MouseEventHandler, useEffect, useRef, useState } from 'react';
import ReactDOM from 'react-dom';
import { ScrollDivToRef, FilterMessages, ScrollToRef, Timeout } from './Utilities'
import { ChatMessage } from './components/Messages';
import { LoadingAnimation } from './components/LoadingAnimation';
import { Input } from './components/Input';
import { ModelSelect, ModelsProps } from './components/ModelSelect';
import { Configuration } from './global';
import { LoadModels, GetReply, CreateChat, GetConversation, GetConversations, DeleteConversation, Message, ModelReply } from './infrastructure/Api'
import { PlusSvg } from './components/Svg';
import { SidebarButton } from './components/SidebarButton';

import './App.css';

function App2() {
    const defaultModels: ModelsProps[] = [
      { label: "gpt-3.5-turbo", value: "gpt-3.5-turbo" },
    ];
  
    const defaultMessage: Message[] = [ 
      {role: "system", content: Configuration.GPT_BEHAVIOUR},
    ] 
  
    const currentChatId = window.localStorage.getItem('chat_id');
  
    const [input, setInput] = useState("");

    const [model, setModel] = useState(defaultModels[0].value);
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
      // await Timeout(500);
      // let id;
      // if(chatid) {
      //   id = chatid;
      // } else { 
      //   id = chatId;
      // }
      // let form = document.getElementById(`chat-${id}`);
      // console.log(form);
      // if(form) { 
      //   ScrollToRef(form);
      // }
  }
  
    async function NewChat(){
      window.localStorage.removeItem('chat_id');
  
      const response = await CreateChat();
      setChatLog(response);
  
      console.log("newChat response", response);
      if(response.chat_id){
        window.localStorage.setItem('chat_id', String(response.chat_id));
        setChatId(String(response.chat_id))
      }
      LoadChats();
    }
  
    async function DeleteChat(chatid: string | undefined) {
        window.localStorage.removeItem('chat_id');

        if(chatid) {
            await DeleteConversation(chatid);
            console.log("deleted");
            console.log(chatid);
        }
    
        LoadChats();

        if(currentChatId) {
            console.log("currentChatId:", currentChatId);
            LoadChatLog(Number(currentChatId));
          }
      }

    async function LoadChat(chatId: number) {
      const response = await GetConversation(chatId);
    
      console.log("loadChat response", response);
      if(response && response.chat_id){
        window.localStorage.setItem('chat_id', String(response.chat_id));
        setChatId(String(response.chat_id));
        setChatLog(response);
        ScrollNavbar(response.chat_id)
      }
    }
  
    async function LoadChats() { 
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
  
    async function LoadChatLog(chatId: number) {
        const storedConversation = await GetConversation(chatId);
  
        if(storedConversation){
          setChatLog(storedConversation);
        } else {
          window.localStorage.removeItem('chat_id');
  
          if(!storedConversations){
            await NewChat()
          } else { 
            setChatId(null)
          }
        }
       }

    useEffect(() => {
      async function loadModels() {
        const models = await LoadModels();
        setModels(models);
      }
  
      loadModels();
      LoadChats();
  
      if(currentChatId) {
        console.log("currentChatId:", currentChatId);
        LoadChatLog(Number(currentChatId));
      }
    }, [])
  
    async function OnSelect(e: React.ChangeEvent<HTMLSelectElement>) {
      e.preventDefault
      setModel(e.target.value);
      window.localStorage.setItem("model", e.target.value);
      console.log(e.target.value);
    }

    async function handleSubmit(e: React.SyntheticEvent<HTMLFormElement>) {
      e.preventDefault();
  
      if (input.length === 0) {
        return;
      }
  
      setIsLoading(true);
  
      if(chatId === null || chatId === undefined){
        await NewChat();
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
  
      if(newChatLog.chat_description == "new chat") {
          await LoadChats()
      }
  
      setIsLoading(false);
    }
  
    return (
    <div className='h-full'>

        <SidebarButton />

        <aside id="default-sidebar" className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
            <div className="h-full px-3 py-4 overflow-y-auto bg-gray-800">
                <div className="flex items-center pl-2.5 mb-5">
                    <img src={process.env.PUBLIC_URL + '/gptalk_logo.png'} className="h-6 mr-3 sm:h-7" alt="GPTalk Logo" />
                    <span className="self-center text-xl font-semibold whitespace-nowrap text-white">GPTalk</span>
                </div>
                <div>
                    <ul className="space-y-2 mb-2">
                        <li>
                            <a href="#" onClick={NewChat} className="flex items-center p-2 text-base font-normal rounded-lg text-white hover:bg-gray-700">
                            <PlusSvg />
                            <span className="ml-3">New Chat</span>
                            </a>
                        </li>
                    </ul>

                    {/* <select onChange={(e) => OnSelect(e)} id="models" className="block py-2.5 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 appearance-none focus:outline-none focus:ring-0 peer rounded-l rounded-r">
                      { models.map((model, i) => ( 
                          <option key={i} value={model.value} defaultValue={model.value}>{model.label}</option>
                      )) 
                      }
                    </select> */}
                    <ModelSelect 
                      models={models} 
                      defaultModel={defaultModels[0].value}
                      setModel={setModel}/>
                    <ul className="block py-2.5 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 appearance-none focus:outline-none focus:ring-0 peer rounded-l rounded-r">
                        {
                        storedConversations
                            .map((modelReply, i) => (
                                <li id={`chat-${modelReply.chat_id}`}>
                                    <div className='flex'>
                                        <button onClick={() => LoadChat(Number(modelReply.chat_id))} 
                                            className={
                                                `flex w-full cursor-pointer items-center p-2 text-base font-normal rounded-l
                                                    ${ modelReply.chat_id == chatId && "bg-gray-700"} 
                                                     text-white hover:bg-gray-600 border-l border-b border-t border-gray-700`}
                                            key={modelReply.chat_id} 
                                            >
                                        <svg aria-hidden="true" className="flex-shrink-0 w-6 h-6 transition duration-75 text-gray-400 group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clipRule="evenodd"></path></svg>
                                        <span className="flex-1 w-36 ml-3 whitespace-nowrap truncate text-left">{ modelReply.chat_description}</span>
                                    
                                        </button>
                                        { 
                                            // modelReply.chat_id != chatId &&
                                            <button onClick={() => DeleteChat(modelReply.chat_id)} className={`flex-none items-center justify-center px-1 text-sm font-medium rounded-r ${ modelReply.chat_id == chatId && "bg-gray-700"} hover:bg-red-800 text-gray-300 border-r border-b border-t border-gray-700`}>
                                            <svg className="text-gray-400"  width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <line x1="18" y1="6" x2="6" y2="18" />  <line x1="6" y1="6" x2="18" y2="18" /></svg>
                                            </button>
                                        }
                                        { modelReply.chat_id == chatId && <div ref={chatRefs} />}
                                    </div>

                            </li>
                            ))
                        }
                    </ul>
                </div>
            </div>
        </aside>

        <div className="sm:ml-64 calc-height mb-64 overflow-auto">
            {
          chatLog
            .messages
            .filter((message: Message) => FilterMessages(message, "system"))
            .map((message, i) => (
              <ChatMessage key={i} {...message}/> 
          ))
        }

    { 
    !chatId && 
    
    <div className="flex items-center justify-center h-full">
      <div className="flex items-center pl-2.5 mb-5">
          <img src={process.env.PUBLIC_URL + '/gptalk_logo.png'} className="h-16 mr-3 sm:h-12" alt="GPTalk Logo" />
          <span className="self-center text-2xl font-semibold whitespace-nowrap text-white">GPTalk</span>
      </div>
    </div>
    }
    <div ref={messagesEndRef} />
        {isLoading && <LoadingAnimation />}

        </div>

        { chatId && 
        
        <div className='fixed sm:ml-64 justify-center p-4 footer-input inset-x-0 bottom-0'>
          <div className='w-screen'>

              <form id="chat-form" onSubmit={handleSubmit}>
                  <textarea 
                  rows={1}
                  className='bg-gray-500 text-white placeholder-gray-700 text-sm rounded-lg ring-gray-500 focus:ring-gray-500 border-0 block w-full p-2.5' 
                  onKeyDown={onEnterPress}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}>
                  </textarea >
                  <button id="chat-button" type="submit" style={{display: "none"}}>
                  </button>
              </form>
              { chatLog.total_tokens > 0 && 
                <div className="text-white text-center text-base font-thin">Total Tokens: {chatLog.total_tokens}</div>
            }
          </div>
        </div>
        }

    </div>

  );
}

export default App2
