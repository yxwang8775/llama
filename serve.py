# torchrun --nproc_per_node 1 example_chat_completion.py \
#     --ckpt_dir /cpfs01/shared/public/public_hdd/llmeval/model_weights/llama2/model_weights/chat/llama-2-7b-chat/ \
#     --tokenizer_path /cpfs01/shared/public/public_hdd/llmeval/model_weights/llama2/model_weights/chat/tokenizer.model \
#     --max_seq_len 512 --max_batch_size 6

from flask import Flask, request, jsonify
from llama import Llama, Dialog

app = Flask(__name__)

# Initialize the model and tokenizer outside of the route to load them only once
generator = None


def initialize_generator(ckpt_dir: str, tokenizer_path: str, max_seq_len: int = 512, max_batch_size: int = 8):
    global generator
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size
    )


@app.route('/chat', methods=['POST'])
def chat():
    # Get the input from the request
    dialogs = request.json.get("dialogs")
    temperature = request.json.get("temperature", 0.6)
    top_p = request.json.get("top_p", 0.9)
    max_gen_len = request.json.get("max_gen_len")

    # Generate a response using the model
    results = generator.chat_completion(
        dialogs,
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p
    )

    # Return the assistant's response
    dialog = dialogs[0]  # assuming a single dialog for simplicity
    result = results[0]
    dialog.append(result['generation'])
    return jsonify(dialog)


if __name__ == '__main__':
    # Initialize the generator here (using sample paths for now)
    initialize_generator(
        '/cpfs01/shared/public/public_hdd/llmeval/model_weights/llama2/model_weights/chat/llama-2-7b-chat/',
        '/cpfs01/shared/public/public_hdd/llmeval/model_weights/llama2/model_weights/chat/tokenizer.model')
    app.run(debug=True)