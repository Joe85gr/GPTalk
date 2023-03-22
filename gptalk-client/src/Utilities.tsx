import { Message } from "./infrastructure/Api";

export const ScrollDivToRef = (ref:  React.RefObject<HTMLDivElement>) => {
    if(ref && ref.current)
    {ref.current.scrollIntoView({ behavior: "smooth" })}
   }

   export const ScrollToRef = (ref: HTMLElement) => {
    if(ref)
    {ref.scrollIntoView({ behavior: "smooth" })}
   }

export function FilterMessages(message: Message, filter: string) { 
    return (message.role != filter); 
} 

export function Timeout(delay: number) {
    return new Promise( res => setTimeout(res, delay) );
}