"""Streamlit GUI for the respiration-rate project. M1: audio preparation."""

from hashlib import sha256

import streamlit as st

from dsp import AUDIO_CONFIG, prepare_audio, read_wav


def main():
    st.set_page_config(page_title="Respiration Rate Estimator", page_icon="🎙️", layout="centered")
    st.title("Respiration Rate Estimator")
    st.caption("An educational audio and digital signal processing project.")
    st.write("Record or upload a breathing sample to begin.")
    st.info("This version prepares audio. Breathing-rate estimation will be added next.")

    with st.expander("Recording tips and supported files"):
        st.write(
            "Use a quiet room and keep your microphone position steady. "
            "Record 30 to 120 seconds of comfortable breathing; aim for about 60 seconds. "
            "Avoid talking or touching the microphone during the recording."
        )
        st.write("Supported: mono or stereo WAV, at least 8000 Hz, up to 50 MB.")
        st.caption("Educational demonstration only. Not a medical diagnostic tool.")

    input_method = st.radio("Audio source", ["Upload WAV", "Record audio"], horizontal=True)
    if input_method == "Upload WAV":
        uploaded = st.file_uploader("Choose a breathing recording", type=["wav"], key="uploaded_audio")
    else:
        st.caption("Allow microphone access if your browser asks, then stop recording when finished.")
        uploaded = st.audio_input("Record a breathing sample", key="recorded_audio")

    audio_bytes = uploaded.getvalue() if uploaded is not None else None
    token = (input_method, sha256(audio_bytes).hexdigest()) if audio_bytes else None
    if st.session_state.get("audio_token") != token:
        st.session_state["audio_token"] = token
        st.session_state.pop("prepared_audio", None)

    if uploaded is None:
        st.button("Analyze audio", disabled=True)
        st.caption("Your recording will appear here with playback and file details.")
        return

    try:
        recording = read_wav(audio_bytes)
    except ValueError as error:
        st.session_state.pop("prepared_audio", None)
        st.error(str(error))
        st.button("Analyze audio", disabled=True)
        return

    st.subheader("Your recording")
    st.caption(uploaded.name)
    st.audio(audio_bytes, format="audio/wav")
    duration_column, rate_column, channel_column = st.columns(3)
    duration_column.metric("Duration", f"{recording['duration_s']:.1f} s")
    rate_column.metric("Sample rate", f"{recording['source_sample_rate']:,} Hz")
    channel_column.metric("Channels", "Mono" if recording["channels"] == 1 else "Stereo")

    if st.button("Analyze audio", type="primary"):
        st.session_state.pop("prepared_audio", None)
        try:
            with st.spinner("Preparing your audio..."):
                st.session_state["prepared_audio"] = prepare_audio(recording)
        except ValueError as error:
            st.error(str(error))

    prepared = st.session_state.get("prepared_audio")
    if prepared is not None:
        st.success("Audio prepared successfully.")
        st.write(
            f"The audio is mono at {prepared['sample_rate']:,} Hz with the DC offset removed. "
            "The original recording is kept without peak normalization."
        )
        with st.expander("Preparation details"):
            st.write(f"Prepared samples: {len(prepared['audio']):,}")
            st.write(f"Prepared duration: {prepared['duration_s']:.2f} seconds")
            st.write(f"Removed DC offset: {prepared['dc_offset']:+.6f}")
            st.write("Resampled: " + ("Yes" if prepared["resampled"] else "Not needed"))
            st.caption(f"Processing sample rate: {AUDIO_CONFIG['sample_rate']:,} Hz")

    st.caption("Educational demonstration only. Not a medical diagnostic tool.")


if __name__ == "__main__":
    main()
