import React from 'react';
import ReactMarkdown from "react-markdown";
import { SvgError, SvgGptLogo } from "./Svg";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, nord, coldarkDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { CodeProps } from "react-markdown/lib/ast-to-react";
import { Message } from '../infrastructure/Api'


export interface IConversation {
  chat_id: number;
  messages: Array<Message>;
  total_tokens: number;
}
  
 export const ChatMessage: React.FC<Message>  = (message) => {

    let bg = "";

    if (message.role === "assistant")
    {
      bg = 'bg-gray-700';
    }
    else if (message.role === "error") {
      bg = 'bg-red-200 bg-opacity-50';
    }

    return (
      <div className={`${bg} mr-2`}> 
        <div className="p-8 text-left flex">
          <div className="self-center rounded-full w-6 h-6 text-white bg-black">
              {
                (message.role === "assistant" && <SvgGptLogo />) ||
                (message.role === "error" && <SvgError />)
              }
          </div>
          <div className="pr-8 pl-8 text-white overflow-x-auto">
            <ReactMarkdown 
              children={message.content}
              components={{
                code({node, inline, className, children, style, ...props} : CodeProps) {
                  const match = /language-(\w+)/.exec(className || '');
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div" {...props}
                    >
                    {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  )
                }
              }}/>

          </div>
        </div>
      </div>
    )
  }

  