import { IMessage } from "./components/Messages";

export const ScrollToBottom = (endRef:  React.RefObject<HTMLDivElement>) => {
    if(endRef && endRef.current)
    {endRef.current.scrollIntoView({ behavior: "smooth" })}
   }

export function FilterMessages(message: IMessage, filter: string) { 
    return (message.role != filter); 
} 