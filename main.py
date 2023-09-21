import streamlit as st
import winsound
import textwrap
import webrtcvad
from IPython.display import HTML
from generate_response import response_function
from speech_func import Speech


# Create an instance of the Speech class
speech_functions = Speech()

# vad = webrtcvad.Vad()
# vad.set_mode(1)  # Aggressiveness: 0 (least aggressive) to 3 (most aggressive)



def main(stop_keyword="restart", exit_keyword="exit"):
    st.title("🤖 Intelligent Voice Assistant")

    conversation_history = []

    # Create a Streamlit sidebar
    st.sidebar.title("Settings")
    st.sidebar.write("Press the Start button and ask me a question. I will respond.")

    if st.sidebar.button("Start"):
        st.sidebar.write(
            "Note:  You can start your question over by saying Restart during question input..."
        )  # Instruction section
        st.sidebar.write(
            "You can end the chat session by saying 'Exit'"
        )  # Instruction section

        welcome_message = "Hi Balaji, How can i assist you today"

        st.markdown(
            f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
            f"{welcome_message}</div>",
                unsafe_allow_html=True,
            )
        
        speech_functions.text_to_speech(welcome_message)


        while True:
            st.text("🤖 Listening...")
            winsound.Beep(800, 200)  # Play a beep sound when ready for input

            input_text = speech_functions.transcribe_audio()

            if not input_text:
                continue

            wrapped_input = textwrap.fill(input_text, width=90)
            indented_input = "\n".join(
                [
                    "<div style='text-align: left;'>" + line + "</div>"
                    for line in wrapped_input.splitlines()
                ]
            )

            st.markdown(
                f"<div style='padding: 30px;'>"
                f"<div style='background-color: blue; padding: 10px; border-radius: 5px; color: white; text-align: left;'>"
                f"{indented_input}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

            if stop_keyword.lower() in input_text.lower():
                st.text("Restarting prompt...")
                conversation_history = []
                continue

            if exit_keyword.lower() in input_text.lower():
                end_message  = (
                    "Thank you for using our IT support AI assistant.\n"
                    "If you have any more questions or need assistance in the future, feel free to reach out. Have a great day!\n"
                )
                st.markdown(
                f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
                f"{end_message}</div>",
                unsafe_allow_html=True,
                )
                
                speech_functions.text_to_speech(end_message)
                

                break

            response_text = response_function.generate_response(input_text, conversation_history)
            print(response_text)
            wrapped_response = textwrap.fill(response_text, width=70)
            indented_response = "\n".join(
                [
                    "<div style='text-align: left;'>" + line + "</div>"
                    for line in wrapped_response.splitlines()
                ]
            )

            st.markdown(
                f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
                f"{indented_response}</div>",
                unsafe_allow_html=True,
            )

            # synthesize_and_play_speech(response_text)
            speech_functions.text_to_speech(response_text)
            conversation_history.append({"role": "user", "content": input_text})
            conversation_history.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main(stop_keyword="restart", exit_keyword="exit")





