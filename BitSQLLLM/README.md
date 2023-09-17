# Download model weights

1. Install Git large file system (`git-lfs`)
  - [Github LFS](https://github.com/git-lfs/git-lfs/blob/main/INSTALLING.md)
  ```bash
  # Linuxmint 20.3 Una based on Ubuntu Focal
  curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | os=ubuntu dist=focal sudo -E bash
  ```

- [llama github](https://github.com/facebookresearch/llama/blob/main/README.md)

1. Accept their license. [Meta AI](https://ai.meta.com/resources/models-and-libraries/llama-downloads/)

2. Request permission to meta-llama on [Huggingface](https://huggingface.co/meta-llama)
  - Each models

3. Clone the [llama repo](https://github.com/facebookresearch/llama)

4. Run `example_chat_completion.py`

```bash
torchrun --nproc_per_node 1 example_chat_completion.py --ckpt_dir Llama-2-7b-chat/ --tokenizer_path ./Llama-2-7b-chat/tokenizer.model --max_seq_len 512 --max_batch_size 6
```
