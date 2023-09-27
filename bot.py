import gradio as gr

from conversation import create_conversation

qa = create_conversation()



def add_text(history, text):
    history = history + [(text, None)]
    return history, ""


def bot(history):
    res = qa(
        {
            'question': history[-1][0], #question/query
            'chat_history': history[:-1]
        }
    )
    history[-1][1] = res['answer'] #answer/result
    return history


with gr.Blocks() as demo:

    layout_html = """

    <div style="display: flex; justify-content: space-between;">
        <!-- Title on the right with bold font -->
        <div style="text-align: right; font-size: 30px; font-weight: bold;">
            <img src="https://previews.dropbox.com/p/thumb/AB-PyD8is5yeHQgycVrRUQzNeITUkOfDS3-pFcRMw0EbAEIcHpLOT0BxAQcEyRNNu-W5dToxFB2Xhe2k_jk0do_9Yz_Dg5ySKeF6zez3LkguMJBOfL8qM9TIKKiW1xiTkiNhi5K6nmjJqdJOpj3u4t4bpNAT5CF8G0xnJq9qhWrl7nct2ByLGqEDmTEny1KnO5CtR9nAIw_GQgD_llmGKxLXPJo7MNEbHV7XJo8ZRyo5sMUZzvNeNgyyu_IlXU7wssRhr0ElDv_rZEcVoDOZwpsRiCBfwBXGTfG9pVGrmywdWJAh7SqHR_3xeahpKHxT34rXQvolCnSVza0fCmxLg9ty/p.png" width="500" height="60" valing>
        </div>

        <!-- Contributors on the left -->
        
        <div style="display: flex; align-items: center;">
            <!-- First contributor -->
            <div style="text-align: center; margin-right: 20px;">
                <img src="https://media.licdn.com/dms/image/D4E03AQHvA2g0l7EGZw/profile-displayphoto-shrink_800_800/0/1683950699469?e=1695859200&v=beta&t=z6kxsGk5oDtOFSDldFg8RBfIF2PzgxX4s4oTIguLNAA" width="100" height="100" style="border-radius: 50%; border: 3px solid #555;">
                <div style="margin-top: 5px;">Fouad Trad</div>
                <div style="font-size: 12px;">PhD Candidate, ECE</div>
            </div>
            
            <!-- Second contributor -->
            <div style="text-align: center; margin-right: 20px;">
                <img src="https://media.licdn.com/dms/image/D4E03AQHdtNgClMJTpw/profile-displayphoto-shrink_400_400/0/1686741936251?e=1695859200&v=beta&t=8gMwmgJ8eIDVL8slCUQ1kJzrpTMZNd4ex9G8PBEiStM" width="100" height="100" style="border-radius: 50%; border: 3px solid #555;">
                <div style="margin-top: 5px;">Lara Baltaji</div>
                <div style="font-size: 12px;">MSBA Candidate, OSB</div>
            </div>
            
            <!-- Third contributor -->
            <div style="text-align: center;">
                <img src="https://media.licdn.com/dms/image/D4E03AQESnig11Xme7w/profile-displayphoto-shrink_400_400/0/1685007548003?e=1695859200&v=beta&t=hzl0RulHPLtHeG-BXJCAJ56U3H0MLMWEwKuRkZwIrpI" width="100" height="100" style="border-radius: 50%; border: 3px solid #555;">
                <div style="margin-top: 5px;">Ali Hashem</div>
                <div style="font-size: 12px;">MSBA Candidate, OSB</div>
            </div>
        </div>
        
        
    </div>
    """
    gr.HTML(layout_html)
    chatbot = gr.Chatbot([], elem_id="chatbot",
                         label='MSBA316 CourseMate').style(height=420)
    with gr.Row():
        with gr.Column(scale=0.80):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter",
            ).style(container=False)
        with gr.Column(scale=0.10):
            submit_btn = gr.Button(
                'Submit',
                variant='primary'
            )
        with gr.Column(scale=0.10):
            clear_btn = gr.Button(
                'Clear',
                variant='stop'
            )

    txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
        bot, chatbot, chatbot
    )

    submit_btn.click(add_text, [chatbot, txt], [chatbot, txt]).then(
        bot, chatbot, chatbot
    )

    clear_btn.click(lambda: None, None, chatbot, queue=False)

if __name__ == '__main__':
    demo.queue(concurrency_count=3)
    demo.launch()