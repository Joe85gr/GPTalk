import React from 'react';
import Select from 'react-select'

interface Props {
    models: ModelsProps[];
    defaultModel: string;
    setModel: (model: string) => void;
}

export interface ModelsProps { 
        label: string;
        value: string;
    }

export const ModelSelect: React.FC<Props> = (props) => {
    return (
        <Select 
        theme={(theme) => ({
          ...theme,
          borderRadius: 5,
          colors: {
            ...theme.colors,
            primary25: '#cecece',
            primary: 'cecece',
          },
        })}
        options={props.models} 
        defaultInputValue={props.defaultModel}
        onChange={(e) => {
        if(e) { 
            console.log(e);
            console.log(e.value);
            props.setModel(e.value) 
        }
      }}/>
    )
    }