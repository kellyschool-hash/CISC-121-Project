import random
import gradio as gr

MAX_STEPS = 200

#Stage 1: Generate List

def generate_list():
    arr = random.sample(range(1, 50), 10)
    display = f"Random Unsorted List:\n{arr}"
    return display, arr


#Stage 2: Insertion Sort Trace

def insertion_sort_on_state(user_number, custom_list_str, arr_state):
    #Decide which list to use: custom (if provided) or generated
    arr = None
    source_label = ""

    # 1)Try custom list if the textbox is not empty
    if custom_list_str is not None and str(custom_list_str).strip() != "":
        try:
            # split on comma or space
            tokens = [t for t in str(custom_list_str).replace(",", " ").split() if t]
            arr = [int(t) for t in tokens]
            source_label = "Custom List"
        except ValueError:
            # if parsing fails, return an error
            error_msg = "Please enter only integers separated by commas or spaces (e.g., 5, 2, 9, 1)."
            return (
                error_msg,
                *["" for _ in range(MAX_STEPS)],
                "Invalid custom list input."
            )

    # 2)If no custom list, fall back to generated arr_state
    if arr is None:
        if not arr_state:
            list_msg = "Please either generate a list or enter your own list first."
            return (
                list_msg,
                *["" for _ in range(MAX_STEPS)],
                "No list to sort."
            )
        arr = arr_state[:]
        source_label = "Random Unsorted List"

    #Display of the original list
    original_display = f"{source_label}:\n{arr}"

    n = len(arr)

    #Optional number to track
    highlight = None
    if user_number is not None:
        try:
            highlight = int(user_number)
        except:
            highlight = None

    steps: list[str] = []

    def log_step(msg):
        steps.append(msg)

    #INSERTION SORT 
    for i in range(1, n):
        current_value = arr[i]
        j = i - 1
    
        log_step(
            f"Pass {i}: take value {current_value} from index {i} "
            f"and insert it into the sorted part on the left (indices 0..{i-1})."
        )
        while j >= 0:
            log_step(f"Compare {current_value} with arr[{j}] = {arr[j]}.")
    
            if arr[j] > current_value:
                log_step(
                    f"Shift: {arr[j]} > {current_value}, thus moving {arr[j]} right (index {j} -> {j+1}) to make room for {current_value}."
                )
                arr[j + 1] = arr[j]
                j -= 1
            else:
                log_step(
                    f"No shift needed: {current_value} ≥ {arr[j]} (stop shifting)."
                )
                break
    
        log_step(f"Insert {current_value} at position {j+1} of array")
        arr[j + 1] = current_value
    
        msg = f"After pass {i}: {arr}"
        if highlight is not None and highlight in arr:
            msg += f" | Tracked number {highlight} is at index {arr.index(highlight)} of array"
    
        log_step(msg)

    #Build final message
    if highlight is not None and highlight in arr:
        final_msg = f"Sorted: {arr}, tracked number {highlight} is at index {arr.index(highlight)} of array"
    elif highlight is not None:
        final_msg = f"Sorted: {arr}, tracked number {highlight} is not in the list"
    else:
        final_msg = f"Sorted: {arr}"

    # Convert steps into updates for each step box
    step_updates = []
    for i in range(MAX_STEPS):
        if i < len(steps):
            step_updates.append(
                gr.update(
                    value=steps[i],
                    visible=True,
                )
            )
        else:
            step_updates.append(
                gr.update(
                    value="",
                    visible=False,
                )
            )

    return original_display, *step_updates, final_msg


# UI

theme = gr.themes.Ocean(
    primary_hue="pink",
    neutral_hue="slate",
)

with gr.Blocks(title="Insertion Sort Visualizer") as demo:
    gr.Markdown(
        """
        # Insertion Sort Visualizer

        **Option A:** Click **Generate List** to create a random list of 10 numbers.  
        **Option B:** Type your own list of integers (comma or space separated).  
        Then Pick a number from the list to track, then click **Run Insertion Sort**.
        """
    )

    arr_state = gr.State([])

    # LEFT SIDE COLUMN holds Generate List AND the custom list box
    with gr.Row():
        with gr.Column(scale=1):
            gen_btn = gr.Button("Generate List", variant="secondary")
            custom_list_box = gr.Textbox(
                label="Or enter your own list (e.g., 5, 2, 9, 1, 7)",
                lines=1,
                placeholder="5, 2, 9, 1, 7",
            )

        # RIGHT SIDE COLUMN holds the number input + Run button
        with gr.Column(scale=1):
            user_number = gr.Number(
                label="Pick a number from the list to track it's index (optional)",
                value=None,
                precision=0
            )
            run_btn = gr.Button("Run Insertion Sort", variant="primary")

    list_box = gr.Textbox(label="List", lines=2, interactive=False)
    step_boxes = [
        gr.Textbox(
            label=f"Step {i+1}",
            lines=3,
            interactive=False,
            visible=False,
        )
        for i in range(MAX_STEPS)
    ]
    result_box = gr.Textbox(label="Final Result", lines=1, interactive=False)

    # Wire Generate button
    gen_btn.click(
        generate_list,
        inputs=[],
        outputs=[list_box, arr_state]
    )


    run_btn.click(
        insertion_sort_on_state,
        inputs=[user_number, custom_list_box, arr_state],
        outputs=[list_box, *step_boxes, result_box],
    )

demo.launch(theme=theme)