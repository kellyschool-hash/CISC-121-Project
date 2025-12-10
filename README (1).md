---
title: insertion-sort-visualizer
emoji: 👀
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 6.1.0
app_file: app.py
pinned: false
---
***Algorithm Name: Insertion Sort Visualizer***

*Why was Insertion Sort Chosen?*

I chose to implement Insertion Sort because the visualizer provided in class felt difficult to follow and did not clearly show how values move during the sorting process. By building my own visualizer, I was able to present each comparison, shift, and insertion step in a way that is much easier to understand.

Insertion Sort is also an excellent algorithm for learning purposes because:


- It mirrors how humans naturally sort items (like cards in a hand).
- It allows students to observe step-by-step changes in the array.
- It is simple enough for beginners, yet still demonstrates key algorithmic ideas such as comparisons, shifting, and incremental ordering.
- Its behavior is easy to visualize, making it ideal for an educational tool.

Overall, creating my own visualizer provides a clear, intuitive, and accessible representation of the algorithm, helping students understand not just the final result but the process of sorting itself.

*Overall Problem*

An interactive way to teach and visualize insertion sort:
- Show how the algorithm takes one element at a time.
- Show how it compares and shifts elements.
- Let the user follow what happens to a specific number they care about.
- Present feedback in plain English instead of just code.

*How the Code Solves It*
1. Generate List
      - Use Python’s random.sample to create 10 unique integers between 1 and 49.
      - Show this list in a read-only textbox labeled List.
2. Insertion Sort with Logging
      - Copy the generated list into a local arr so the original can still be displayed.
      - Run standard insertion sort.
    	At each pass:
    	- Log what “current value” we are inserting.
    	- Log which values it is being compared to.
    	- Log when shifting stops.
    	- Log the full array after the pass, plus where the tracked number ended up (if provided).
3. User Interface (Gradio)
      - gen_btn triggers generate_list.
      - run_btn triggers insertion_sort_on_state.
    	Multiple textboxes show:
    	- The original unsorted list.
    	- Up to MAX_STEPS messages describing the passes.
    	- A final result summary.


***Computational Thinking: Four Pillars***

*Decomposition*
Break the problem into smaller, manageable subtasks:
  1. State management
      - arr_state (Gradio State) stores the current unsorted list between button clicks.
  2. List generation
      - Function generate_list():
      - Produces data: a list of integers.
      - Produces display: a string Random Unsorted List:\n[...].
  3. Sorting logic
    	Function insertion_sort_on_state():
        	- Validates that the list exists.
        	- Reads the optional user-provided number to track.
        	- Runs insertion sort on a copy of the list.
  4. Step logging
      - Inner helper log_step(msg):
      - Appends explanatory messages to steps until MAX_STEPS is reached.
  5. Presentation
    	Return values from insertion_sort_on_state are mapped to:
     
        	- list_box (original list text)
        	- A series of step_boxes (detailed messages)
        	- result_box (summary of sorted list and tracked index)

*Pattern Recognition*

Insertion sort itself has a clear repeating pattern:

	For each index i from 1 to n-1:
      1. Take the value at index i (called current_value).
      2. Look left from j = i - 1 down to 0:
         - While items are bigger than current_value, shift them one spot to the right.
      3. Insert current_value in the first spot where it’s not smaller than the item to its left.

*Abstraction*
- hide low-level details and present a simplified mental model:
    1. Hidden from user:
      - Python syntax (for loops, indices, list assignments).
      - Internal storage (arr_state, steps).
      - Edge cases like empty lists and type casting.
	2. Shown to user:
      - Natural language explanations:
      - “Compare 27 with arr[2] = 43.”
      - “Stop shifting: 27 ≥ arr[1] = 35.”
    	Full array after each pass:
      - They see how the left part becomes sorted over time.
    3. Simple description in the UI:
      - “Press ‘Generate List’ to generate a random list. Pick a number to track…”
- Abstraction allows the app to be used by someone who doesn’t know Python at all—they just need to understand that we are sorting numbers and following the steps.

*Algorithmic Thinking*

  ```

PSEUDOCODE FOR INSERTION SORT VISUALIZER


CONSTANT MAX_STEPS = 200

------------------------------------------------------------
PROCEDURE GenerateList()
    arr ← randomly select 10 unique integers from range 1..49
    display_text ← "Random Unsorted List:\n" + arr
    RETURN (display_text, arr)
END PROCEDURE
------------------------------------------------------------



------------------------------------------------------------
PROCEDURE InsertionSortOnState(user_number, custom_list_str, arr_state)
    arr ← null
    source_label ← ""


    # Stage A: Determine which list to use


    IF custom_list_str is not empty THEN
        TRY
            tokens ← replace commas with spaces in custom_list_str
            tokens ← split tokens on spaces
            arr ← convert each token to an integer
            source_label ← "Custom List"
        CATCH conversion error
            RETURN ("Error: invalid list input",
                    empty_step_boxes(MAX_STEPS),
                    "Invalid custom list input.")
        END TRY
    END IF

    IF arr = null THEN
        IF arr_state is empty THEN
            RETURN ("Please generate a list or enter your own.",
                    empty_step_boxes(MAX_STEPS),
                    "No list to sort.")
        ELSE
            arr ← copy of arr_state
            source_label ← "Random Unsorted List"
        END IF
    END IF

    original_display ← source_label + ":\n" + arr
    n ← length(arr)


    # Stage B: Optional tracked number

    highlight ← null
    IF user_number provided THEN
        TRY highlight ← integer(user_number)
        CATCH → highlight remains null
    END IF


    # Stage C: Perform insertion sort while logging steps

    steps ← empty list

    FUNCTION LogStep(text)
        append text to steps
    END FUNCTION

    FOR i FROM 1 TO n-1 DO
        current_value ← arr[i]
        j ← i - 1

        LogStep("Pass " + i + ": take value " + current_value +
                " from index " + i + " and insert into sorted portion.")

        WHILE j ≥ 0 DO
            LogStep("Compare " + current_value +
                    " with arr[" + j + "] = " + arr[j])

            IF arr[j] > current_value THEN
                LogStep("Shift: " + arr[j] + " > " + current_value +
                        ", move " + arr[j] + " to index " + (j+1))
                arr[j+1] ← arr[j]
                j ← j - 1
            ELSE
                LogStep("No shift needed: " + current_value +
                        " ≥ " + arr[j] + " (stop shifting).")
                BREAK
            END IF
        END WHILE

        LogStep("Insert " + current_value +
                " at position " + (j+1))
        arr[j+1] ← current_value

        message ← "After pass " + i + ": " + arr

        IF highlight ≠ null AND highlight is in arr THEN
            index ← index of highlight in arr
            message ← message + 
                       " | Tracked number " + highlight +
                       " is at index " + index
        END IF

        LogStep(message)
    END FOR


    # Stage D: Final summary message

    IF highlight ≠ null AND highlight in arr THEN
        final_msg ← "Sorted: " + arr +
                     ", tracked number " + highlight +
                     " is at index " + index_of(highlight)
    ELSE IF highlight ≠ null THEN
        final_msg ← "Sorted: " + arr +
                     ", tracked number " + highlight +
                     " is not in the list"
    ELSE
        final_msg ← "Sorted: " + arr
    END IF


    # Stage E: Map steps into UI step boxes

    step_updates ← empty list

    FOR i FROM 0 TO MAX_STEPS-1 DO
        IF i < length(steps) THEN
            append update(value = steps[i], visible = true)
        ELSE
            append update(value = "", visible = false)
        END IF
    END FOR

    RETURN (original_display,
            step_updates...,
            final_msg)

END PROCEDURE
------------------------------------------------------------

UI SUMMARY 


User clicks "Generate List":
    - Calls GenerateList
    - Displays the list
    - Saves arr_state

User enters list or number (optional) and clicks "Run Insertion Sort":
    - Calls InsertionSortOnState
    - Shows:
         - Chosen list
         - A dynamic number of step boxes
         - Final result (sorted array + tracked number index)
------------------------------------------------------------
  ```
  

Time complexity:
  - Worst case: O(n²) comparisons/shifts (e.g., when the list is in descending order).
  - Best case: O(n) when the list is already sorted (no shifting inside the while loop).



***Test And Verify***

*Random generated list with tracked number* 

![IMG_4821](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/IHWxiI0WBdPRqkjjfg4Kt.png)
![IMG_5622](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/F1V_RvGJoNwjrUhiM5nbq.png)


*Custom list with tracked number* 

![IMG_0095](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/RA1QKpdL5UUv6Sc4e1R1a.png)
![IMG_5542](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/Wog6wKVrUi_dj1jjyw7Ry.png)

*Random list with no tracked number*

![IMG_0574](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/siJQv-u99q0BngSB8VNg-.png)
![IMG_3873](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/08GjH4JYdyCUoTAH01BJ-.png)

*Custom list with no tracked number*

![IMG_1448](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/t04_GSp-DDaxsczRUwmbL.png)
![IMG_3226](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/o9AVwoQcwCHL2WSiGtm8B.png)

*Custom list with invalid input*

![IMG_3598](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/CMZiKSUMoO2yDSMZfWbqQ.png)

*Random list with tracked number not in list*

![IMG_0150](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/4UJ3x566ZomJ8zwq5Dhqh.png)
![IMG_9859](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/XX16K43-vHcuMhYAHyE09.png)

*Custom list with tracked number not in list*

![IMG_3086](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/ca_wKA9QJVHezb7mQp-t3.png)
![IMG_1400](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/jijKqe2K_DvLNFfaMRdM2.png)

*Custom list with spaces instead of commas*

![IMG_9120](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/mZdwWnlssVaGUMOuAcotV.png)
![IMG_3984](https://cdn-uploads.huggingface.co/production/uploads/6937499f6b3d367be94c90ca/vwi6ObGWm9EYzf8aM1eJf.png)


***Steps to Run***
1. Install dependencies:


   ```
     pip install gradio
   ```

   
2. Save code as app.py
3. Run code:
     python app.py

***Hugging Face link***: https://huggingface.co/spaces/KellyHaTran/Insertion-Sort-Visualizer

***Author & Acknowledgment***


Author: Kelly Ha Tran


Algorithm implemented: Insertion Sort


Language / Frameworks:
- Python 
- Gradio 