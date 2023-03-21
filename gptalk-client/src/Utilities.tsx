import { Message } from "./infrastructure/Api";

export const ScrollToBottom = (endRef:  React.RefObject<HTMLDivElement>) => {
    if(endRef && endRef.current)
    {endRef.current.scrollIntoView({ behavior: "smooth" })}
   }

export function FilterMessages(message: Message, filter: string) { 
    return (message.role != filter); 
} 