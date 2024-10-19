import os
import random
import gradio as gr
import pandas as pd

def get_csv_files():
    csv_files = [f for f in os.listdir('./classroom') if f.endswith('.csv')]
    return csv_files

def load_layout(layout_input, csv_layout_input: gr.Dropdown):
    print(csv_layout_input.value)
    layout_file = csv_layout_input.value
    layout = pd.read_csv(f'./classroom/{layout_file}', header=None)
    layout_input.value = layout.values.tolist()
    return pd.DataFrame(layout.values.tolist())

def generate_seating_chart(layout: pd.DataFrame, students: str):
    rows, cols = layout.shape
    students = students.split('\n')
    random.shuffle(students)
    seating_chart_df = layout.copy()
    seating_chart_df = seating_chart_df.astype(object)
    for i in range(rows):
        for j in range(cols):
            if layout.iloc[i, j] == 1:
                if len(students) > 0:
                    seating_chart_df.iloc[i, j] = students.pop(0)
                else:
                    seating_chart_df.iloc[i, j] = ''
            elif layout.iloc[i, j] == 0:
                seating_chart_df.iloc[i, j] = ''
    return seating_chart_df

def save_seating_chart(seating_chart_df: pd.DataFrame):
    seating_chart_df.to_csv('seating_chart.csv', index=False, header=False)
    gr.Info('座位表已下載至 seating_chart.csv')

if __name__ == '__main__':
    csv_files = get_csv_files()
    default_layout = pd.read_csv(f'./classroom/{csv_files[0]}', header=None).values.tolist()
    with gr.Blocks() as app:
        gr.Markdown('# 隨機座位表生成器')
        with gr.Row():
            with gr.Column():
                gr.Markdown('## 輸入教室佈局')
                layout_input = gr.Dataframe(headers=None, row_count=10, col_count=10, datatype='str', value=default_layout)
                csv_layout_input = gr.Dropdown(choices=csv_files, label='選擇內建教室佈局')
                csv_layout_input.change(load_layout, inputs=[layout_input, csv_layout_input], outputs=[layout_input])
            with gr.Column():
                gr.Markdown('## 輸出座位表')
                layout_output = gr.Dataframe(headers=None, datatype='str', value=default_layout)
                download_button = gr.Button('下載座位表')
                download_button.click(save_seating_chart, inputs=[layout_output])
        students_input = gr.Textbox(label='學生清單', lines=10, placeholder='輸入學生清單，每行一個學生')
        submit_button = gr.Button('生成座位表')
        submit_button.click(generate_seating_chart, inputs=[layout_input, students_input], outputs=[layout_output])
    app.launch()