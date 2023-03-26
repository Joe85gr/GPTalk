import React from 'react';
import ReactMarkdown from "react-markdown";
import { SvgError, SvgGptLogo } from "./Svg";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { CodeProps } from "react-markdown/lib/ast-to-react";
import { Message } from '../infrastructure/client'
// import { CodeCopyBtn } from './CopyButton'

export interface IConversation {
  chat_id: number;
  messages: Array<Message>;
  total_tokens: number;
}
  
interface Props {
  children: React.ReactNode
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

    // const Pre = ({children}: Props) => <pre className="relative mb-4 mt-4 overflow-x-auto">
    //     <CodeCopyBtn>{children}</CodeCopyBtn>
    //     {children}
    // </pre>

    const customStyle = {
      padding: "20px",
      }

    return (
      <div className={`${bg} mr-2`}> 
        <div className="sm:p-8 p-4 text-left sm:mr-5 flex">
          <div className="self-center rounded-full w-6 h-6 text-white bg-gray-700">
              {
                (message.role === "assistant" && <SvgGptLogo />) ||
                (message.role === "error" && <SvgError />)
              }
          </div>
          <div className="pr-8 sm:pl-8 pl-4 text-white text-base overflow-x-auto">
            <ReactMarkdown 
              children={message.content}
              components={{
                // pre: Pre,
                code({node, inline, className, children, style, ...props} : CodeProps) {
                  const match = /language-(\w+)/.exec(className || '');
                  if (match) { 
                   }
                  return !inline && match ? (
                    <SyntaxHighlighter
                      showLineNumbers
                      showInlineLineNumbers
                      
                      customStyle={customStyle}
                      style={vscDarkPlus}
                      language={match[1]}
                      PreTag="div" {...props}>
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

  