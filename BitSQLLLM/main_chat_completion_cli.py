# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import List, Dict, Optional

import fire

from llama.llama import Llama, Dialog
from llama.llama.tokenizer import Tokenizer


def get_token_len(tokenizer: Tokenizer, content: str) -> int:
    return len(tokenizer.encode(content, bos=True, eos=True))


def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    """
    Entry point of the program for generating text using a pretrained model.

    Args:
        ckpt_dir (str): The directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): The path to the tokenizer model used for text encoding/decoding.
        temperature (float, optional): The temperature value for controlling randomness in generation.
            Defaults to 0.6.
        top_p (float, optional): The top-p sampling parameter for controlling diversity in generation.
            Defaults to 0.9.
        max_seq_len (int, optional): The maximum sequence length for input prompts. Defaults to 512.
        max_batch_size (int, optional): The maximum batch size for generating sequences. Defaults to 8.
        max_gen_len (int, optional): The maximum length of generated sequences. If None, it will be
            set to the model's max sequence length. Defaults to None.
    """
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    tokenizer = Tokenizer(model_path=tokenizer_path)

    prompt = 'Hello! How can I assist you?'

    history: List[Dict[int, Dialog]] = [{'token': len(tokenizer.encode(prompt, bos=True, eos=True)) + len(tokenizer.encode('user', bos=True, eos=True)),
                                         'dialog': {'role': 'system',
                                                    'content': prompt}
                                        }]

    print(f'{history[0]["dialog"]["role"]}: {history[0]["dialog"]["content"]}')

    while True:
        while True:
            prompt = input('You: ').strip()
            if not len(prompt):
                continue
            token_len = get_token_len(tokenizer, f'User: {prompt}')
            if token_len > max_seq_len*0.7:
                print(f'System: You exceed max_seq_len({max_seq_len*0,7:d}). Please type prompt less')
                continue
            break
        history.append({'token': token_len,
                        'dialog': {'role': 'user',
                                   'content': prompt}})

        tokens_len = 0
        cut = -1
        for i in range(len(history)-1, -1, -1):
            tokens_len = tokens_len + history[i]['token']
            if tokens_len > max_seq_len:
                cut = i
                break
        if cut >= 0:
            print(f'System forgot {cut+1} previous history')
            for _ in range(cut+1):
                history.pop(0)

        print([[entry['dialog'] for entry in history]])
        results = generator.chat_completion(
            [[entry['dialog'] for entry in history]],  # type: ignore
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )
        
        response = results[0]['generation']

        history.append({'token': get_token_len(tokenizer, f'Assistant: {response["content"]}'),
                        'dialog': {'role': 'assistant',
                                   'content': response['content']}})

        print(f'{history[-1]["dialog"]["role"]}: {history[-1]["dialog"]["content"]}')
        print()


if __name__ == "__main__":
    fire.Fire(main)
