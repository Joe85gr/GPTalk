import React from 'react';
import ReactMarkdown from "react-markdown";
import { SvgError, SvgGptLogo } from "./Avatars";
import "./Messages.css";
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
    return (
      <div className={`chat-message ${message.role}`}>
        <div className="chat-message-center">
          <div className={`chat-avatar ${message.role}`}>
              {
                (message.role === "assistant" && <SvgGptLogo />) ||
                (message.role === "error" && <SvgError />)
              }
          </div>
          <div className="message">
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

  